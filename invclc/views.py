from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice,DeletedInvoice,ModifiedInvoice
from .forms import InvoiceForm
from django.http import JsonResponse,HttpResponseServerError,HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q,F
from django.utils import timezone
from authentication.models import CustomUser,Person
from datetime import datetime
import csv
import json
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.management import call_command
from django.http import HttpResponse
from decimal import Decimal
from datetime import datetime
from openpyxl import Workbook
from import_export.resources import ModelResource
from import_export.fields import Field
from tablib import Dataset
from import_export.results import RowResult
from import_export.formats.base_formats import DEFAULT_FORMATS,XLSX
from import_export import resources
from .forms import UploadFileForm


# views.py
from django.http import JsonResponse
from .models import Invoice

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_content'):
        csv_content = request.FILES['csv_content'].read().decode('utf-8')
        # Assuming you have a way to get the current user (e.g., request.user)
        current_user = request.user
        # Create or update the invoice with the CSV content
        invoice = Invoice.objects.create(
            user=current_user,
            csv_content=csv_content  # Assuming your Invoice model has a field named csv_content
        )
        return JsonResponse({'message': 'CSV content uploaded successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required(login_url='/')
def exports_to_csv(request):
    currentuser = request.user
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Import_DataCSV_{currentuser}.csv"'

    writer = csv.writer(response)
    writer.writerow(['IN. No.', 'Total Amount', 'Last Payment Date', 'Payed', 'Paid/Pending'])
    for obj in Invoice.objects.filter(user=request.user):
        if obj.balance_amount == 0:
            status = 'paid'
        else:
            status = 'pending'
        writer.writerow([obj.invoice_number, obj.invoice_amount, obj.today_date, obj.payment_amount, status])

    return response


def exports_to_xlsx(request):
    currentuser = request.user
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Import_DataXLSX_{currentuser}.xlsx"'

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['IN. No.', 'Total Amount', 'Last Payment Date', 'Payed', 'Paid/Pending'])
    for obj in Invoice.objects.filter(user=request.user):
        if obj.balance_amount == 0:
            status = 'paid'
        else:
            status = 'pending'
        worksheet.append([obj.invoice_number, obj.invoice_amount, obj.today_date, obj.payment_amount, status])

    workbook.save(response)
    return response


@login_required(login_url='/')
def exports_to_json(request):
    currentuser = request.user
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="Import_DataJSON_{currentuser}.json"'
    call_command('dumpdata', 'invclc.Invoice', format='json', stdout=response)  
    return response

@login_required(login_url='/')
def index_view(request):
    current_user = request.user
    invoices = Invoice.objects.filter(user=current_user)
    payment_details = invoices.filter().order_by('-id')
    q_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    search_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), Q(payment_amount=0)).order_by('-id')
    payed_details = invoices.filter(balance_amount=0.00).order_by('-id')
    try:
        unique_code = Person.objects.get(user = request.user)
        unique_id = unique_code.UniqueId
    except Person.DoesNotExist:
        unique_code = "Please Update Your Profile"
        unique_id = "Please Update Your Profile"
        
    DeleteHistory = DeletedInvoice.objects.filter(user=current_user).order_by('-id')
    if not DeleteHistory.exists():
        DeleteHistory = "N Deletion Found"
        
    ModifiedHistory = ModifiedInvoice.objects.filter(user = current_user).order_by('-id')
    if not ModifiedHistory.exists():
        ModifiedHistory = "No Updatation Found"
     
# print(history_entries.history_user)
    
    if request.method == 'POST':
        query = request.POST.get('payment_list')
        if query is not None:
            lookups = Q(pharmacy_name__icontains=query)
            payment_details = payment_details.filter(lookups)
        if query == 'all':
            payment_details = invoices.order_by('-id')

        paied = request.POST.get('payed')
        if paied is not None:
            search_payed = Q(pharmacy_name__icontains=paied)
            payed_details = payed_details.filter(search_payed)
        if paied == 'all':
            payed_details = invoices.filter(balance_amount=0.00).order_by('-id')

        q = request.POST.get('q')
        if q is not None:
            q_payed = Q(pharmacy_name__icontains=q)
            q_details = q_details.filter(q_payed)
        if q == 'all':
            q_details = invoices.order_by('-id')

        search = request.POST.get('search')
        if search is not None:
            search_data = Q(pharmacy_name__icontains=search)
            search_details = search_details.filter(search_data)
        if search == 'all':
            search_details = invoices.order_by('-id')

        invoice_form = InvoiceForm(request.POST)
        if invoice_form.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect("index")
        else:
            error_message = invoice_form.errors.get('invoice_number', 'Invoice Number Must Be Unique')
            messages.error(request, error_message)
            
    else:
        invoice_form = InvoiceForm()

    context = {'form':invoice_form,
               'payment':payment_details,
               'payed_details':payed_details,
               'q':q_details,
               'search':search_details,
               'uniqueid':unique_id,
               'DeleteHistory':DeleteHistory,
               'ModifiedHistory':ModifiedHistory,
               }
    return render(request,'invclc/index.html',context)


@login_required(login_url='/')
def update_view(request):
    invoices = Invoice.objects.filter(user=request.user).order_by('-id')
    return render(request, 'invclc/update.html', {'invoices': invoices})

@login_required(login_url='/')
def delete_page(request):
    invoices = Invoice.objects.filter(user=request.user).order_by('-id')
    return render(request, 'invclc/delete.html', {'invoices': invoices})

@login_required(login_url='/')
def check_view(request,id):
    userInvoice = Invoice.objects.get(id = id)
    if userInvoice.pharmacy_name:
        user_title = userInvoice.pharmacy_name.title()
    else:
        user_title = "Unknown"

    invoices = Invoice.objects.all().filter(user=request.user).filter(id=id).order_by('-id')
    return render(request, 'invclc/check.html', {'invoices': invoices,'user_title':user_title})


@login_required(login_url='/')
def edit_view(request, id):
    Invoice_edit = Invoice.objects.get(id=id)
    if request.method == 'POST':
        edit_form = InvoiceForm(request.POST, instance=Invoice_edit)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request,"You got it ")
            return redirect("home")
        else:   
            messages.error(request,"Please Make Sure You Select the today ")
        
    # Convert the invoice_date to dd/mm/yyyy format
    invoice_date_str = Invoice_edit.invoice_date.strftime('%B %d, %Y')
    invoice_date_obj = datetime.strptime(invoice_date_str, '%B %d, %Y')
    formatted_invoice_date = invoice_date_obj.strftime('%d/%m/%Y')
    Invoice_edit.invoice_date = formatted_invoice_date
    
    context = { 
        # 'today_date': formatted_today_date,
        'invoice': Invoice_edit
    }
   
    return render(request, 'invclc/edit.html', context)



@login_required(login_url='/')
def create_view(request):
    form = InvoiceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            create_form = form.save(commit = False)
            create_form.user = request.user
            create_form.save()
            return redirect('index')
        else:
            messages.error(" Invoice Number Must be Unique")
    return render(request, 'invclc/create.html', {'form': form})


@login_required(login_url='/')
def delete_view(request, pk):
    invoice = get_object_or_404(Invoice,id=pk)
    invoice.delete()
    return redirect('index')
        
class InvoiceResource(ModelResource):
    class Meta:
        model = Invoice
        fields = ('user', 'pharmacy_name', 'invoice_number', 'invoice_date', 'balance_amount', 'payment_amount')

@login_required(login_url='/')
def import_view(request):
    try:
        person = Person.objects.get(user=request.user)
        city = person.City
        unique_id = person.UniqueId
        admin_user = CustomUser.objects.filter(is_staff=True).order_by('-date_joined')[:1]
        admin_person = Person.objects.get(user=admin_user)
        
        user = request.user
        data = Invoice.objects.filter(user=request.user).order_by('id')
    except Exception as e:
        return HttpResponse("Update Your Profile", e)
    
    
    context = {
        'datas': data,
        'admin_data': admin_user,
        'city': city,
        'admin_person': admin_person,
        'user': user,
        'unique_id': unique_id,
    }
    return render(request, 'invclc/import-export.html', context)

@login_required(login_url = '/')
def payment_view(request,payment_id):
    invoices = Invoice.objects.get(id=payment_id)
    return render(request, 'invclc/payment.html', {'payment': invoices})


@login_required(login_url='/')
def staticspage_view(request):
    current_user = Invoice.objects.filter(user=request.user)
    # Total Amomunt Calculation ..
    all_invoice_amounts = current_user.values_list('invoice_amount', flat=True)
    total_amount = sum(all_invoice_amounts)
    
    # Total Paid Amount Calculation ..
    all_paid_amount = current_user.values_list('payment_amount', flat=True)
    payment_amount = sum(all_paid_amount)
    
    # Total Balance Amount
    all_balance_amount = current_user.values_list('balance_amount', flat=True)
    balance_amount = sum(all_balance_amount)
    
    context = {
        'total_amount': total_amount,
        'payment_amount':payment_amount,
        'balance_amount': balance_amount,
        }
    return render(request, 'invclc/static.html',context)

@login_required(login_url='/')
def checkmore_view(request):
    current_user = request.user
    invoices = Invoice.objects.filter(user=current_user, balance_amount=0.00).order_by('-id')
    return render(request, 'invclc/checkmore.html',{'invoices': invoices})

@login_required(login_url='/')
def paymore_view(request):
    current_user = request.user
    invoices = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    return render(request, 'invclc/paymore.html',{'invoices': invoices})

@login_required(login_url='/')
def updatemore_view(request):
    current_user = request.user
    invoices = Invoice.objects.filter(user = current_user).order_by('-id')
    return render(request, 'invclc/updatemore.html',{'invoices': invoices})

@login_required(login_url='/')
def unpaid_debt(request):
    current_user = request.user
    invoices = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), Q(payment_amount=0)).order_by('-id')
    return render(request, 'invclc/unpaid_debt.html',{'invoices': invoices})

@require_POST
def update_invoice(request, invoice_id):
    try:
        data = json.loads(request.body)
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        
        # Update the fields that don't require special handling
        invoice.pharmacy_name = data.get('pharmacy_name', invoice.pharmacy_name)
        invoice.invoice_amount = Decimal(data.get('invoice_amount', invoice.invoice_amount))
        invoice.invoice_date = data.get('invoice_date', invoice.invoice_date)
        invoice.balance_amount = Decimal(data.get('balance_amount', invoice.balance_amount))

        # Handle balance_amount separately
        invoice_date = data.get('invoice_date', invoice.invoice_date)
        balance_amount = data.get('balance_amount', invoice.balance_amount)

        # Perform the necessary conversions
        invoice_date = parse_date(invoice_date)
        balance_amount = Decimal(balance_amount) if balance_amount is not None else None

        # Update the invoice_date and balance_amount fields
        invoice.invoice_date = invoice_date

        # Check if balance_amount is not None before updating
        if balance_amount is not None:
            # Update balance_amount based on the formula in your model
            invoice.payment_amount = invoice.invoice_amount - balance_amount
        else:
            # If balance_amount is None, set it to invoice.invoice_amount
            invoice.payment_amount = invoice.invoice_amount

        # Save the updated Invoice
        invoice.save()
        
        modified_invoice = ModifiedInvoice(
            user=request.user,
            modified_pharmacy=invoice.pharmacy_name,
            modified_Invoice_number=f"{invoice.invoice_number}_{timezone.now().timestamp()}",
            modified_Invoice_date=invoice.invoice_date,
            modified_Total_amount=invoice.invoice_amount,
            modified_balance=invoice.balance_amount,
            modified_payment=invoice.payment_amount,
            modified_today_date=invoice.today_date
        )

        # Save the DeletedInvoice object
        modified_invoice.save()

        return JsonResponse({'status': 'success', 'message': 'Invoice updated successfully'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def parse_date(date_string):
    date_formats = ['%b. %d, %Y', '%d/%m/%Y', '%d-%m-%y', '%B %d, %Y']

    for date_format in date_formats:
        try:
            return datetime.strptime(date_string, date_format).date()
        except ValueError:
            pass

    raise ValueError("Date string does not match any expected format")

# Example usage:
try:
    result = parse_date("June 10, 2024")
except ValueError as e:
    messages.error(" Date Formate Not Accessable")


# @require_POST
# def update_invoice(request, invoice_id):
#     invoice = get_object_or_404(Invoice, pk=invoice_id)
    
#     form = InvoiceForm(request.POST, instance=invoice)

#     if form.is_valid():
#         form.save()
#         return JsonResponse({'status': 'success', 'message': 'Invoice updated successfully'})
#     else:
#         errors = form.errors.as_json()
#         return JsonResponse({'status': 'error', 'message': errors})
    
@login_required(login_url='/')
def delete_invoice(request, invoice_id):
    try:
        # Check if the invoice exists
        invoice = Invoice.objects.get(pk=invoice_id)

        # Create a DeletedInvoice object with a unique number (using timestamp)
        deleted_invoice = DeletedInvoice(
            user=request.user,
            pharmacy=invoice.pharmacy_name,
            number=f"{invoice.invoice_number}_{timezone.now().timestamp()}",
            date=invoice.invoice_date,
            amount=invoice.invoice_amount,
            balance=invoice.balance_amount,
            payment=invoice.payment_amount,
            today_date=invoice.today_date
        )

        # Save the DeletedInvoice object
        deleted_invoice.save()

        # Delete the Invoice object
        invoice.delete()

        return JsonResponse({'message': 'Invoice deleted successfully'})
    
    except Invoice.DoesNotExist:
        return JsonResponse({'error': 'Invoice not found'}, status=404)

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error deleting invoice with id {invoice_id}: {str(e)}")
        
        return JsonResponse({'error': f'Error deleting invoice: {str(e)}'}, status=500)

    
@require_POST
def pay_invoice(request, invoice_id):
    
    # TODO: For more Details Check Logic.txt File
    try:
        invoice = get_object_or_404(Invoice, id=invoice_id)

        data = json.loads(request.body)
        updated_payment_amount = Decimal(data.get('payment_amount', invoice.payment_amount))

        # Adding the previous payment_amount and Updated payment_amount and Saved into Payment_amount
        invoice.payment_amount = updated_payment_amount + invoice.payment_amount

        if invoice.payment_amount >= invoice.invoice_amount:
            invoice.payment_amount = invoice.invoice_amount

        if invoice.balance_amount <= 0:
            invoice.balance_amount = 0

        invoice.save()

        # Check the action type (Pay or Save)
        action_type = data.get('action_type', 'Pay')

        if action_type == 'Save':
            return JsonResponse({'message': 'Invoice saved successfully'})
        else:
            return JsonResponse({'message': 'Invoice updated successfully'})

    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

@require_POST
def payment_invoice(request,payment_id):
    # TODO: For more Details Check Logic.txt File
    try:
        invoice = get_object_or_404(Invoice, id=payment_id)

        data = json.loads(request.body)

        pay_amount = Decimal(data.get('payment_amount', invoice.payment_amount))
        
        invoice.payment_amount = pay_amount + invoice.payment_amount

        if invoice.payment_amount >= invoice.invoice_amount:
            invoice.payment_amount = invoice.invoice_amount

        if invoice.balance_amount <= 0:
            invoice.balance_amount = 0

        invoice.save()
        
        # Check the action type (Pay or Save)
        action_type = data.get('action_type', 'Pay')

        if action_type == 'Save':
            return JsonResponse({'message': 'Invoice saved successfully'})
        else:
            return JsonResponse({'message': 'Invoice updated successfully'})

    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)