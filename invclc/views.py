from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice,DeletedInvoice,ModifiedInvoice,TrackingPayment,Invitation
from .forms import InvoiceForm
from django.http import JsonResponse,HttpResponseServerError,HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q,F
from django.utils import timezone
from authentication.models import CustomUser,Person,Notification
from datetime import datetime
import csv
import json
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.management import call_command
from decimal import Decimal
from openpyxl import Workbook
from import_export.resources import ModelResource
from import_export.fields import Field
from tablib import Dataset
from import_export.results import RowResult
from import_export.formats.base_formats import DEFAULT_FORMATS,XLSX
from import_export import resources
from .forms import UploadFileForm
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import openpyxl
import logging

logger = logging.getLogger(__name__)
def upload_csv(request):
    
    check_user = None
        
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Collaborating Error : ", a)
            

            
        if request.method == 'POST' and request.FILES.get('file'):
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                if file.name.endswith(('.csv')):
                    try:
                        csv_data = file.read().decode('utf-8').splitlines()
                        csv_reader = csv.DictReader(csv_data)
                        
                        current_user = request.user
                        
                        for row in csv_reader:
                            # Convert date string to datetime object
                            try:
                                invoice_date = datetime.strptime(row['invoice_date'], '%d/%m/%Y').date()
                            except ValueError:
                                invoice_date = datetime.strptime(row['invoice_date'], '%d-%m-%Y').date()
                            
                            # Convert string values to integers
                            invoice_amount = int(row['invoice_amount'])
                            payment_amount = int(row['payment_amount'])
                            
                            # Calculate balance amount
                            balance_amount = invoice_amount - payment_amount
                            
                            # Get the current date and time
                            current_date = datetime.now().date()
                            current_time = datetime.now().time()
                            
                            # Create Invoice object for each row in the CSV file
                            if str(request.user) == check_user:
                                invoice = Invoice.objects.create(
                                    user=collaborator_admin,
                                    pharmacy_name=row['pharmacy_name'],
                                    invoice_number=row['invoice_number'],
                                    invoice_date=invoice_date,
                                    invoice_amount=invoice_amount,
                                    payment_amount=payment_amount,
                                    balance_amount=balance_amount,
                                    today_date=current_date,  # Use current date
                                    current_time=current_time,  # Use current time
                                    updated_by=row['updated_by']
                                )
                            else:
                                invoice = Invoice.objects.create(
                                    user=current_user,
                                    pharmacy_name=row['pharmacy_name'],
                                    invoice_number=row['invoice_number'],
                                    invoice_date=invoice_date,
                                    invoice_amount=invoice_amount,
                                    payment_amount=payment_amount,
                                    balance_amount=balance_amount,
                                    today_date=current_date,  # Use current date
                                    current_time=current_time,  # Use current time
                                    updated_by=row['updated_by']
                                )

                        
                        return JsonResponse({'message': 'CSV Data uploaded successfully'})
                    except Exception as e:
                        logger.exception("Error processing CSV file")
                        return JsonResponse({'error': f'Error processing CSV file: {str(e)}'}, status=500)
                else:
                    return JsonResponse({'error': 'File format not supported. Please upload a CSV file.'}, status=400)
            else:
                return JsonResponse({'error': 'Form is not valid'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        logger.exception("Error in upload_csv view")
        return JsonResponse({'error': 'Server error'}, status=500)


@login_required(login_url='/')
def exports_to_csv(request):
    check_user = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Collaborating Error : ", a)
    except Exception as e:
        return messages.error(request,"Error in Exporting CSV : ", e)
    
    if check_user == str(request.user):
        try:
            currentuser = request.user
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Import_DataCSV_{currentuser}.csv"'

            writer = csv.writer(response)
            writer.writerow(['invoice_number','invoice_amount', 'payment_amount','updated_by','updated_date', 'Paid/Pending Status'])
            for obj in Invoice.objects.filter(user=collaborator_admin ):
                if obj.balance_amount == 0:
                    status = 'paid'
                else:
                    status = 'pending'
                writer.writerow([obj.invoice_number, obj.invoice_amount,obj.payment_amount,obj.updated_by, obj.today_date,  status])

            return response
        except Exception as e:
            return messages.error(request,"Collaborating Error : ", e)
    else:
        try:
            currentuser = request.user
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Import_DataCSV_{currentuser}.csv"'

            writer = csv.writer(response)
            writer.writerow(['invoice_number','invoice_amount', 'payment_amount','updated_by','updated_date', 'Paid/Pending Status'])
            for obj in Invoice.objects.filter(user=currentuser ):
                if obj.balance_amount == 0:
                    status = 'paid'
                else:
                    status = 'pending'
                writer.writerow([obj.invoice_number, obj.invoice_amount,obj.payment_amount,obj.updated_by, obj.today_date,  status])

            return response
        except Exception as a:
            return messages.error(request,"Collaborating Error : ", a)


def exports_to_xlsx(request):   
    check_user = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Collaborating Error : ", a)
    except Exception as e:
        return messages.error(request,"Error in exports_to_xlsx : ", e)
        
    if check_user == str(request.user):
        currentuser = request.user
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="ImportData{currentuser}.xlsx"'

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(['IN. No.', 'Total Amount', 'Last Payment Date', 'Payed', 'Paid/Pending'])
        for obj in Invoice.objects.filter(user=collaborator_admin):
            if obj.balance_amount == 0:
                status = 'paid'
            else:
                status = 'pending'
            worksheet.append([obj.invoice_number, obj.invoice_amount, obj.today_date, obj.payment_amount, status])

        workbook.save(response)
        return response

    else:
        currentuser = request.user
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="ImportDataXLSX_{currentuser}.xlsx"'

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
    check_user = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Something Wrong Whlie Exporting Json ", a)
    except Exception as e:
        return messages.error(request,"Something Wrong Whlie Exporting Json ", e)

        
    if check_user == str(request.user):
        invoices = Invoice.objects.filter(user=collaborator_admin)
        json_data = serialize('json', invoices)
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="invoices_{collaborator_admin}.json"'
        
        return response
    else:
        current_user = request.user
        invoices = Invoice.objects.filter(user=current_user)
        json_data = serialize('json', invoices)
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="invoices_{current_user.username}.json"'
        
        return response

@login_required(login_url='/')
def index_view(request):
    current_user = request.user
    invoices = Invoice.objects.filter(user=current_user)
    payment_details = invoices.order_by('-id')
    q_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    search_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), Q(payment_amount=0))
    payed_details = invoices.filter(balance_amount=0.00).order_by('-id')

    check_user = None
    check_admin = None
    unique_code_id = None

    try:
        unique_code = Person.objects.get(user=request.user)
        unique_id = unique_code.UniqueId
    except Person.DoesNotExist:
        unique_id = f"'{request.user}' Please Update Your Profile"

    # try:
    #     collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
    #     for notification in collaborator_requests:
    #         collaborator_request_username = notification.sender.username
    #         get_admin_name = notification.receiver.username
            
    #         collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
    #         collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
    #         for user in collaborator_request_sender:
    #             collaborator_sender_username = user.username
    #             try:
    #                 current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
    #                 if current_user and collaborator_admin:
    #                     check_user = current_user.username
    #                     check_admin = Invoice.objects.filter(user=collaborator_admin).first()
    #                     unique_code_id = Person.objects.get(user=collaborator_admin)
    #             except CustomUser.DoesNotExist:
    #                 messages.error(request, "Something went wrong")
    # except Notification.DoesNotExist:
    #     messages.error(request, "Error occurred in collaborating to User")
        


    DeleteHistory = DeletedInvoice.objects.filter(user=request.user).order_by('-id')

    if not DeleteHistory.exists():
        DeleteHistory = "No Deletion Found"

    ModifiedHistory = ModifiedInvoice.objects.filter(user=request.user).order_by('-id')

    if not ModifiedHistory.exists():
        ModifiedHistory = "No Updatation Found"

    Storename = None

    try:
        Storename = Person.objects.get(user=request.user)
        modifiedStore = Storename.MedicalShopName if Storename and Storename.MedicalShopName else ""
    except Person.DoesNotExist:
        modifiedStore = ""
    
    entryDisable = None
    userProfile = None

    try:
        user_to_check = request.user

        userProfile = Person.objects.get(user=user_to_check)

        if (userProfile.MedicalShopName and
            userProfile.DrugLiceneseNumber1 and
            userProfile.DrugLiceneseNumber2):
            entryDisable = False
        else:
            entryDisable = True
    except Person.DoesNotExist:
        entryDisable = True
        messages.error(request, "Please complete your profile details to access the fields.")

    
    full_paid =None
    edit_paid = None
    partially_paid = None
    debt_paid = None
    delete_history = None
    modified_history = None
    
    admin_invoices = Invoice.objects.filter(user=request.user)
    full_paid = admin_invoices.filter(balance_amount=0.00).order_by('-id')
    edit_paid = admin_invoices.filter().order_by('-id')
    partially_paid = admin_invoices.filter(~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    debt_paid = admin_invoices.filter(~Q(balance_amount=0.00), Q(payment_amount=0))
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = [
                'pharmacy_name', 'invoice_number', 'invoice_date',
                'invoice_amount', 'payment_amount'
            ]
            
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                messages.error(request,f'Missing fields: {", ".join(missing_fields)}')
                return JsonResponse({
                    'success': False,
                    'message': f'Missing fields: {", ".join(missing_fields)}'
                }, status=400)

            # Convert numeric fields from strings to integers or floats
            try:
                invoice_amount = float(data['invoice_amount'])
                payment_amount = float(data['payment_amount'])
                
                if payment_amount > invoice_amount:
                    messages.error(request,'Payment Not Valid')
                    return JsonResponse({
                        'success':False,
                        'message':'Payment Not Valid '
                        },status=400)
                    
            except ValueError:
                messages.error(request,'Invoice amount and payment amount must be numeric')
                return JsonResponse({
                    'success': False,
                    'message': 'Invoice amount and payment amount must be numeric'
                }, status=400)

            # Convert invoice_date to YYYY-MM-DD format
            try:
                invoice_date = datetime.strptime(data['invoice_date'], '%d/%m/%Y').date()
            except ValueError:
                messages.error(request,'Invoice date must be in DD/MM/YYYY format')
                return JsonResponse({
                    'success': False,
                    'message': 'Invoice date must be in DD/MM/YYYY format'
                }, status=400)

            user_to_save =request.user

            
            invoice_data = Invoice(
                user=user_to_save,
                pharmacy_name=data['pharmacy_name'],  # Keep as string
                invoice_number=data['invoice_number'],
                invoice_date=invoice_date,  # Use converted date
                invoice_amount=invoice_amount,  # Convert to float or int
                payment_amount=payment_amount,  # Convert to float or int
                today_date=datetime.now().date(),  # Set to current date
                current_time=datetime.now().time(),  # Set to current time
            )
            invoice_data.updated_by=request.user

            if entryDisable:
                messages.error(request,'Please Fill Up the data in Profile Page')
                return JsonResponse({
                    'success': False,
                    'message': 'Please Fill Up the data in Profile Page'
                }, status=400)
            else:
                invoice_data.save()
            
            tracking_payment = TrackingPayment(
                user=user_to_save,
                Medical_name = data['pharmacy_name'],
                Bill_no = data['invoice_number'],
                Medical_payments = invoice_amount,
                payment_date = datetime.now().date(),
                paying_amount = payment_amount
            )
            tracking_payment.save()
            
            messages.success(request,'Invoice saved successfully!')
            return JsonResponse({'success': True, 'message': 'Invoice saved successfully!'})
        except json.JSONDecodeError:
            messages.error(request,'Invalid JSON data')
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            messages.error(request,str(e))
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    context = {
        'payment': payment_details,
        'payed_details': payed_details,
        'q': q_details,
        'entryDisable':entryDisable,
        'search': search_details,
        'uniqueid': unique_id,
        'DeleteHistory': DeleteHistory,
        'ModifiedHistory': ModifiedHistory,
        'medicalname': None,
        'MedicalStatus': modifiedStore,
        'check_user': check_user,
        'check_admin': check_admin,
        'unique': unique_code_id,
        'current_user': str(request.user),
        'admin_invoice': invoices,
        'full_paid': full_paid,
        'edit_paid': edit_paid,
        'partially_paid': partially_paid,
        'debt_paid': debt_paid
    }
    return render(request, 'invclc/index.html', context)


# def entrydata(request):
#     entryDisable = None
#     try:
#         userProfile = Person.objects.get(user=request.user)
#         if userProfile.MedicalShopName is not None and userProfile.DrugLiceneseNumber1 is not None and userProfile.DrugLiceneseNumber2 is not None:
#             entryDisable = False
#         else:
#             entryDisable = True
#         return JsonResponse({"Entry": entryDisable})
#     except Person.DoesNotExist:
#         entryDisable = True
#         messages.error(request, "Profile not Accessible")
#         return JsonResponse({"error": "This User Profile Not Found"}, status=400)
    
def convert_Medical(shopname):
    
    if shopname and shopname is not None:
        words = shopname.split()
        if len(words) == 2:
            return ''.join(word[0] for word in words).upper()
        elif len(words) == 3:
            return ''.join(word[0] for word in words).upper()
        elif len(words) > 3:
            return ''.join(word[0] for word in words[:3]).upper()
        elif len(words) == 1:
            return words[0][0].upper()
        else:
            return "####"  

@login_required(login_url='/')
def update_view(request):
    invoices = Invoice.objects.filter(user=request.user).order_by('-id')
    return render(request, 'invclc/update.html', {'invoices': invoices})

@login_required(login_url='/')
def delete_page(request):
    invoices = Invoice.objects.filter(user=request.user).order_by('-id')
    return render(request, 'invclc/delete.html', {'invoices': invoices})

@login_required(login_url='/')
def check_view(request, id):
    current_user = request.user
    Storename = None  
    user_title = "Unknown"
    trackingPayment = None
    modifiedStore = None
    
    check_user = None  # Define check_user here
        
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Something Wrong Please Check",a)
            
    except Exception as e:
        return messages.error(request,"Something Wrong ",e)
        
    if str(request.user) == check_user:
        try:
            Storename = Person.objects.get(user=collaborator_admin)
            modifiedStore = convert_Medical(Storename.MedicalShopName)
        except Person.DoesNotExist:
            modifiedStore = "Not Found"
                
        try:
            trackingPayment = TrackingPayment.objects.filter(user=collaborator_admin).order_by('-id')
        except TrackingPayment.DoesNotExist:
            trackingPayment = []
        
        try:
            userInvoice = Invoice.objects.get(id=id, user=collaborator_admin)
            if userInvoice.pharmacy_name:
                user_title = userInvoice.pharmacy_name.title()
        except Invoice.DoesNotExist:
            pass
        
        invoices = Invoice.objects.filter(user=collaborator_admin, id=id).order_by('-id')
        
    else:
        try:
            Storename = Person.objects.get(user=current_user)
            modifiedStore = convert_Medical(Storename.MedicalShopName)
        except Person.DoesNotExist:
            modifiedStore = "Not Found"
                
        try:
            trackingPayment = TrackingPayment.objects.filter(user=request.user).order_by('-id')
        except TrackingPayment.DoesNotExist:
            trackingPayment = []
        
        try:
            userInvoice = Invoice.objects.get(id=id, user=current_user)
            if userInvoice.pharmacy_name:
                user_title = userInvoice.pharmacy_name.title()
        except Invoice.DoesNotExist:
            pass

        invoices = Invoice.objects.filter(user=current_user, id=id).order_by('-id')
    
    context = {
        'invoices': invoices,
        'user_title': user_title,
        'tracking_invoices': trackingPayment,
        'store': modifiedStore,
    }
    return render(request, 'invclc/check.html', context)



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
            messages.error(request,"Invoice Number Must be Unique")
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


# TODO: Import View ..
@login_required(login_url='/')
def import_view(request):
    upload_csv_file = UploadFileForm()
    check_user = None
    data = None
    admin_city = None  # Initialize admin_city variable
    admin_ph = None
    admin_uniqueid = None
    admin_person = None
    admin_email = None
    admin_street = None
    admin_pincode = None
    admin_dl1 = None
    admin_dl2 = None
    user_city =None
    user_ph =None
    unique_id = None
    collaborator_admin = None
    completed_data = None
    previous_data = None
    user_email = None
    user_street = None
    user_pincode = None
    dl1 = None
    dl2 = None

    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Something Wrong Please Check",a)
    except Exception as e:
        return messages.error(request,"Something Wrong",e)
    
    if str(request.user) == check_user:        
        try:
            person = Person.objects.get(user=collaborator_admin)
            unique_id = person.UniqueId
            admin_person = person.user.username
            admin_city = person.City
            admin_street = person.StreetNumber
            admin_pincode = person.Pincode
            admin_dl1 = person.DrugLiceneseNumber1
            admin_dl2 = person.DrugLiceneseNumber2

            get_admin_ph = CustomUser.objects.get(username=collaborator_admin) 
            admin_ph = get_admin_ph.phone_num
            admin_uniqueid = person.UniqueId
            admin_email = get_admin_ph.email

            user = Person.objects.get(user=request.user)
            user_city = user.City
            get_user_ph = CustomUser.objects.get(username=request.user)
            user_ph = get_user_ph.phone_num 
            unique_id = user.UniqueId
            user_email = get_user_ph.email
            user_street = user.StreetNumber
            user_pincode = user.Pincode
            dl1 = user.DrugLiceneseNumber1
            dl2 = user.DrugLiceneseNumber2
            
            data = Invoice.objects.filter(user=collaborator_admin).order_by('id')
            overall_data = Invoice.objects.filter(user=collaborator_admin).order_by('id')
        except Exception as a:
            return messages.error(request,"Something Wrong Please Check",a) 
          
    else:        
        try:
            user = Person.objects.get(user=request.user)
            user_city = user.City            
            get_user_ph = CustomUser.objects.get(username=request.user)
            user_ph = get_user_ph.phone_num 
            unique_id = user.UniqueId
            user_email = get_user_ph.email
            user_street = user.StreetNumber
            user_pincode = user.Pincode
            dl1 = user.DrugLiceneseNumber1
            dl2 = user.DrugLiceneseNumber2

            data = Invoice.objects.filter(user=request.user).order_by('id')
            overall_data = Invoice.objects.filter(user=request.user).order_by('-id')
        except CustomUser.DoesNotExist:
            return messages.error(request, "CustomUser does not exist")
        except Person.DoesNotExist:
            messages.error(request, "Please Update Your Profile and try agin to import export page")
            return redirect("profile")

    user_name = request.user
    if request.method == 'POST':
        completed = request.POST.get('completed', False)
        category = request.POST.get('category', '')
        others = request.POST.get('others', False)
        not_paid = request.POST.get('all',False)
        pharmacy_name = request.POST.get('pharmacyName',False) # Corrected variable name
        
        if str(request.user) == check_user:
            try:
                if completed == 'true':
                    completed_data = list(Invoice.objects.filter(balance_amount=0, user=collaborator_admin).values('invoice_number', 'invoice_amount', 'updated_by', 'today_date', 'payment_amount', 'balance_amount'))
                    return JsonResponse({"completed_data": completed_data})
                elif not_paid == 'true':
                    not_paid_datas = list(Invoice.objects.filter(Q(user=collaborator_admin) &~Q(balance_amount=0.00) &(~Q(balance_amount=F('invoice_amount')) |Q(payment_amount=0))).order_by('-id').values('invoice_number', 'invoice_amount', 'updated_by', 'today_date', 'payment_amount', 'balance_amount'))
                    return JsonResponse({"not_paid_data": not_paid_datas})
                elif category:
                    users_with_category = list(CustomUser.objects.filter(store_type__iexact=category).values('username', 'phone_num', 'email', 'store_type'))
                    return JsonResponse({"category_list": users_with_category})
                elif others and len(others) > 1:
                    otherStores = list(CustomUser.objects.filter(store_type__icontains=others).values('username', 'phone_num', 'email', 'store_type'))
                    if not otherStores:
                        otherStoreType = CustomUser.objects.filter(other_value__icontains=others).exists()
                        if otherStoreType:
                            storeTypeList = list(CustomUser.objects.filter(other_value__icontains=others).values('username', 'phone_num', 'email', 'other_value'))
                            return JsonResponse({"storeTypeList": storeTypeList})
                    return JsonResponse({"otherStores": otherStores}) 
                
                elif pharmacy_name and pharmacy_name != '':
                    try:
                        particular_user_invoices = Invoice.objects.filter(user=collaborator_admin, pharmacy_name=pharmacy_name).values()
                        modified_invoices = []
                        for invoice in particular_user_invoices:
                            modified_invoice = {key.replace('_', ' ').capitalize(): value for key, value in invoice.items() if key not in ['id', 'user_id', 'current_time']}
                            modified_invoices.append(modified_invoice)
                        return JsonResponse({'invoices': modified_invoices})
                    except Invoice.DoesNotExist:
                        return JsonResponse({'error': 'No invoices found for the given pharmacy name'}, status=404)
                
                else:
                    previous_data = list(Invoice.objects.filter(user=collaborator_admin).values('invoice_number', 'invoice_amount', 'updated_by', 'today_date', 'payment_amount', 'balance_amount'))
                    return JsonResponse({"previous_data": previous_data})
                
            except Exception as e:
                return messages.error(request,"Something Wrong Try Again: ",e)
        else:
            try:
                if completed == 'true':
                    completed_data = list(Invoice.objects.filter(balance_amount=0, user=request.user).values('invoice_number', 'invoice_amount', 'updated_by', 'today_date', 'payment_amount', 'balance_amount'))
                    return JsonResponse({"completed_data": completed_data})
                elif not_paid == 'true':
                    not_paid_datas = list(Invoice.objects.filter(Q(user=request.user) &~Q(balance_amount=0.00) &(~Q(balance_amount=F('invoice_amount')) |Q(payment_amount=0))).order_by('-id').values('invoice_number', 'invoice_amount', 'updated_by', 'today_date', 'payment_amount', 'balance_amount'))
                    return JsonResponse({"not_paid_data": not_paid_datas})
                elif category:
                    users_with_category = list(CustomUser.objects.filter(store_type__iexact=category).values('username', 'phone_num', 'email', 'store_type'))
                    return JsonResponse({"category_list": users_with_category})
                elif others and len(others) > 1:
                    otherStores = list(CustomUser.objects.filter(store_type__icontains=others).values('username', 'phone_num', 'email', 'store_type'))
                    if not otherStores:
                        otherStoreType = CustomUser.objects.filter(other_value__icontains=others).exists()
                        if otherStoreType:
                            storeTypeList = list(CustomUser.objects.filter(other_value__icontains=others).values('username', 'phone_num', 'email', 'other_value'))
                            return JsonResponse({"storeTypeList": storeTypeList})
                    return JsonResponse({"otherStores": otherStores}) 
                
                elif pharmacy_name and pharmacy_name != '':
                    try:
                        particular_user_invoices = Invoice.objects.filter(user=request.user, pharmacy_name=pharmacy_name).values()
                        modified_invoices = []
                        for invoice in particular_user_invoices:
                            modified_invoice = {key.replace('_', ' ').capitalize(): value for key, value in invoice.items() if key not in ['id', 'user_id', 'current_time']}
                            modified_invoices.append(modified_invoice)
                        return JsonResponse({'invoices': modified_invoices})
                    except Invoice.DoesNotExist:
                        return JsonResponse({'error': 'No invoices found for the given pharmacy name'}, status=404)
                else:
                    previous_data = list(Invoice.objects.filter(user=request.user).values('invoice_number', 'invoice_amount', 'updated_by', 'today_date', 'payment_amount', 'balance_amount'))
                    return JsonResponse({"previous_data": previous_data})
            except Exception as e:
                return messages.error(request,"Something Wrong Try Again: ",e)

            

    # medicals = []  # Initialize an empty list to store medical shop names

    # for medical_user in overall_medicals:
    #     get_user_profile = medical_user.person
    #     medicals.append(get_user_profile.MedicalShopName)
        
    # print("medicals : ", medicals)

    context = {
        'datas': data,
        # 'medicals':medicals,
        'user_email':user_email,
        'user_street':user_street,
        'user_pincode':user_pincode,
        'dl1':dl1,
        'dl2':dl2,
        'admin_email':admin_email,
        'admin_pincode':admin_pincode,
        'admin_dl1':admin_dl1,
        'admin_dl2':admin_dl2,
        'admin_street':admin_street,
        'completed_data':completed_data,
        'check_user': check_user,
        'request_user': str(request.user),
        'admin_city': admin_city,   
        'admin_ph': admin_ph,
        'admin_id': admin_uniqueid,
        'user_city': user_city,
        'user_ph': user_ph,
        'admin_person': admin_person,
        'user': user_name,
        'unique_id': unique_id,
        'form':upload_csv_file,
        'overall_data':overall_data,
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
    Storename = None
    modifiedStore = None
    trackingPayment = None

    check_user = None  # Define check_user here
        
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Something Wrong Please Check",a)
            
    except Exception as e:
        return messages.error(request,"Something Wrong Please Check",e)
    
    if check_user == str(request.user):
        try:
            Storename = Person.objects.get(user=collaborator_admin)
            modifiedStore = convert_Medical(Storename.MedicalShopName)
        except Person.DoesNotExist:
            modifiedStore = "Not Found"
                
        trackingPayment = TrackingPayment.objects.filter(user=collaborator_admin).order_by('-id')
        invoices = Invoice.objects.filter(user=collaborator_admin, balance_amount=0.00).order_by('-id')
    else:
        try:
            Storename = Person.objects.get(user=current_user)
            modifiedStore = convert_Medical(Storename.MedicalShopName)
        except Person.DoesNotExist:
            modifiedStore = "Not Found"
                
        trackingPayment = TrackingPayment.objects.filter(user=request.user).order_by('-id')
        invoices = Invoice.objects.filter(user=current_user, balance_amount=0.00).order_by('-id')
    
    
    context={
        'invoices': invoices,
        'MedicalStatus':modifiedStore,
        'tracking_invoices':trackingPayment,
    }
    return render(request, 'invclc/checkmore.html',context)


@login_required(login_url='/')
def paymore_view(request):
    current_user = request.user
    check_user = None 
    
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username

            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Something Wrong Please Check",a)
                       
    except Exception as e:
        return messages.error(request,"Something Wrong",e)
    
    if check_user == str(request.user):
        invoices = Invoice.objects.filter(Q(user=collaborator_admin ), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
        trackingPayment = TrackingPayment.objects.filter(user=collaborator_admin).order_by('-id')
    else:
        trackingPayment = TrackingPayment.objects.filter(user=request.user).order_by('-id')
        invoices = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    return render(request, 'invclc/paymore.html',{'invoices': invoices,'tracking_invoices':trackingPayment})

@login_required(login_url='/')
def updatemore_view(request):
    current_user = request.user
    check_user = None 
    collaborator_admin = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Something Wrong Please Check",a)
            
    except Exception as e:
        return messages.error(request,"Something Wrong ",e)
    if collaborator_admin and collaborator_admin is not None:
        invoices = Invoice.objects.filter(user = collaborator_admin).order_by('-id')
    else:
        
        invoices = Invoice.objects.filter(user = current_user).order_by('-id')
    return render(request, 'invclc/updatemore.html',{'invoices': invoices})

@login_required(login_url='/')
def unpaid_debt(request):
    current_user = request.user
    check_user = None 
    collaborator_admin = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    return messages.error(request,"Something Wrong",a)
            
    except Exception as e:
        return messages.error(request,"Something Wrong",e)
    if collaborator_admin is not None:
        invoices = Invoice.objects.filter(Q(user=collaborator_admin), ~Q(balance_amount=0.00), Q(payment_amount=0))
    else:
        invoices = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), Q(payment_amount=0))
    return render(request, 'invclc/unpaid_debt.html',{'invoices': invoices})

def update_invoice(request, invoice_id):
    try:
        data = json.loads(request.body)
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        
        # Update the fields that don't require special handling
        invoice.pharmacy_name = data.get('pharmacy_name', invoice.pharmacy_name)
        invoice.invoice_number = data.get('invoice_number',invoice.invoice_number)
        invoice.invoice_amount = Decimal(data.get('invoice_amount', invoice.invoice_amount))
        invoice.invoice_date = data.get('invoice_date', invoice.invoice_date)
        invoice.balance_amount = Decimal(data.get('balance_amount', invoice.balance_amount))

        # Perform the necessary conversions
        invoice_date = data.get('invoice_date', invoice.invoice_date)
        invoice_date = parse_date(invoice_date)

        # Update the invoice_date field
        invoice.invoice_date = invoice_date

        # Update the payment_amount based on the balance_amount
        invoice.balance_amount = invoice.invoice_amount - invoice.payment_amount

        # Save the updated Invoice
        invoice.save()
        
        check_user = None  # Define check_user here
        
        try:
            collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
            
            for notification in collaborator_requests:
                collaborator_request_username = notification.sender.username
                get_admin_name = notification.receiver.username
                
                collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
                collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
                
                for user in collaborator_request_sender:
                    collaborator_sender_username = user.username
                    try:
                        current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                        if current_user and collaborator_admin:
                            check_user = current_user.username
                    except Exception as a:
                        return messages.error(request,"Something Wrong Please Check",a)
                
        except Exception as e:
            return messages.error(request,"Something Wrong",e)
            
        if check_user == str(request.user):
            modified_invoice = ModifiedInvoice(
                user=collaborator_admin,
                modified_pharmacy=invoice.pharmacy_name,
                modified_Invoice_number=f"{invoice.invoice_number}_{timezone.now().timestamp()}",
                modified_Invoice_date=invoice.invoice_date,
                modified_Total_amount=invoice.invoice_amount,
                modified_balance=invoice.balance_amount,
                modified_payment=invoice.payment_amount,
                modified_today_date=invoice.today_date
            )
        else:
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

        # Save the ModifiedInvoice object
        modified_invoice.save()

        # Display success message
        messages.success(request, "Invoice successfully modified")

        return JsonResponse({'status': 'success', 'message': 'Invoice updated successfully'})
    except json.JSONDecodeError:
        # Handle JSON decoding error
        messages.error(request, "Failed to modify invoice: Invalid JSON data")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    except Exception as e:
        # Handle other exceptions
        messages.error(request, f"Failed to modify invoice: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})


def parse_date(date_string):
    date_string = date_string.strip()
    date_formats = ['%b. %d, %Y', '%d/%m/%Y', '%d-%m-%y', '%B %d, %Y']

    for date_format in date_formats:
        try:
            return datetime.strptime(date_string, date_format).date()
        except ValueError:
            pass

    raise ValueError("Date string does not match any expected format")


    
@login_required(login_url='/')
def delete_invoice(request, invoice_id):
    try:
        # Check if the invoice exists
        invoice = Invoice.objects.get(pk=invoice_id)
        
        check_user = None  # Define check_user here
        
        try:
            collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
            
            for notification in collaborator_requests:
                collaborator_request_username = notification.sender.username
                get_admin_name = notification.receiver.username
                
                collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
                collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
                
                for user in collaborator_request_sender:
                    collaborator_sender_username = user.username
                    try:
                        current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                        if current_user and collaborator_admin:
                            check_user = current_user.username
                    except Exception as a:
                        return messages.error(request,"Something Wrong Please Check",a)
                
        except Exception as e:
            return messages.error(request,"Something Wrong",e)

        # Create a DeletedInvoice object with a unique number (using timestamp)
        if check_user == str(request.user):
            deleted_invoice = DeletedInvoice(
                user=collaborator_admin,
                pharmacy=invoice.pharmacy_name,
                number=f"{invoice.invoice_number}_{timezone.now().timestamp()}",
                date=invoice.invoice_date,
                amount=invoice.invoice_amount,
                balance=invoice.balance_amount,
                payment=invoice.payment_amount,
                today_date=invoice.today_date
            )
        else:
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

        messages.success(request,"Deleted Success")
        return JsonResponse({'message': 'Invoice deleted successfully'})
    
    except Invoice.DoesNotExist:
        messages.erroe(request,"Deletion Failed ")
        return JsonResponse({'error': 'Invoice not found'}, status=404)

    except Exception as e:      
        messages.error(request,f'Error deleting invoice: {str(e)}')
        return JsonResponse({'error': f'Error deleting invoice: {str(e)}'}, status=500)

    
@require_POST
def pay_invoice(request, invoice_id):
    
    # TODO: For more Details Check Logic.txt File
    try:
        invoice = get_object_or_404(Invoice, id=invoice_id)

        data = json.loads(request.body)
        updated_payment_amount = Decimal(data.get('payment_amount', invoice.payment_amount))

        if updated_payment_amount <= 0:
            # Ensure payment amount is positive
            messages.error(request,"Payment amount must be greater than zero")
            return JsonResponse({'error': 'Payment amount must be greater than zero'}, status=422)

        if invoice.payment_amount + updated_payment_amount > invoice.invoice_amount:
            # Check if the total payment exceeds the invoice amount
            messages.error(request,"payment Amount Not Valid..")
            return JsonResponse({'error': 'Total payment exceeds invoice amount'}, status=409)

        invoice.payment_amount += updated_payment_amount
        if invoice.payment_amount >= invoice.invoice_amount:
            invoice.payment_amount = invoice.invoice_amount
            invoice.balance_amount = 0
        else:
            invoice.balance_amount -= updated_payment_amount

        invoice.save()
        
        tracking_payment = TrackingPayment(
            user=invoice.user,
            Medical_name = invoice.pharmacy_name,
            Bill_no = invoice.invoice_number,
            Medical_payments = invoice.payment_amount,
            payment_date = invoice.today_date,
            paying_amount = updated_payment_amount
        )
        
        tracking_payment.save()
        messages.success(request,"payment Success")

        # Check the action type (Pay or Save)
        action_type = data.get('action_type', 'Pay')

        if action_type == 'Save':
            return JsonResponse({'message': 'Invoice saved successfully'})
        else:
            return JsonResponse({'message': 'Invoice updated successfully'})

    except Exception as e:
        messages.error(request,"Payment Falied")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

@require_POST
def payment_invoice(request,payment_id):
    # TODO: For more Details Check Logic.txt File
    try:
        invoice = get_object_or_404(Invoice, id=payment_id)

        data = json.loads(request.body)

        pay_amount = Decimal(data.get('payment_amount', invoice.payment_amount))
        
        if pay_amount <= 0:
            # Ensure payment amount is positive
            messages.error(request,"Payment amount must be greater than zero")
            return JsonResponse({'error': 'Payment amount must be greater than zero'}, status=422)

        if invoice.payment_amount + pay_amount > invoice.invoice_amount:
            # Check if the total payment exceeds the invoice amount
            messages.error(request,"payment Amount Not Valid..")
            return JsonResponse({'error': 'Total payment exceeds invoice amount'}, status=409)
        
        invoice.payment_amount = pay_amount + invoice.payment_amount

        if invoice.payment_amount >= invoice.invoice_amount:
            invoice.payment_amount = invoice.invoice_amount

        if invoice.balance_amount <= 0:
            invoice.balance_amount = 0

        invoice.save()
        
        tracking_payment = TrackingPayment(
            user=invoice.user,
            Medical_name = invoice.pharmacy_name,
            Bill_no = invoice.invoice_number,
            Medical_payments = invoice.payment_amount,
            payment_date = invoice.today_date,
            paying_amount = pay_amount
        )
        
        tracking_payment.save()
        messages.success(request,"payment Success")
        
        # Check the action type (Pay or Save)
        action_type = data.get('action_type', 'Pay')

        if action_type == 'Save':
            return JsonResponse({'message': 'Invoice saved successfully'})
        else:
            return JsonResponse({'message': 'Invoice updated successfully'})

    except Exception as e:
        messages.error(request,"payment Failed",e)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


def empty_csv(request):
    # Define header row
    header = ['pharmacy_name', 'invoice_number', 'invoice_date', 'invoice_amount', 'payment_amount', 'updated_by']
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_data.csv"'

    # Write header row to CSV
    writer = csv.writer(response)
    writer.writerow(header)

    return response

def empty_xlsx(request):
    # Define header row
    header = ['pharmacy_name', 'invoice_number', 'invoice_date', 'invoice_amount', 'payment_amount', 'updated_by']
    
    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write header row to worksheet
    worksheet.append(header)

    # Create HttpResponse object with XLSX content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sample_data.xlsx"'

    # Save workbook to HttpResponse
    workbook.save(response)

    return response

@login_required(login_url='/')
def admin_access(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("Import Data: ", data)

        username = data.get('username','')
        useremail = data.get('useremail','')
        userposition = data.get('userposition','')
        userphonenumber = data.get('userphone','')  # Assuming phone number is part of the data

        # Create and save the invitation instance
        invitation = Invitation(
            user=request.user,
            mail_sendername=request.user.username,
            mail_receiver_name=username,
            mail_receiver_email=useremail,
            mail_receiver_phonenumber=userphonenumber,
            mail_receiver_position=userposition
        )
        invitation.save()
        
        subject = "Invitation to Join Our Platform"
        text_message = f"Dear {username},\n\nYou have been invited to join our platform as a {userposition}. Please use the following details to access your account.\n\nBest regards,\nThe Team"

        # Render the HTML message from a template
        html_message = render_to_string('invitation_email.html', {
            'user_name': username,
            'user_position': userposition,
            'sender_mail': settings.DEFAULT_FROM_EMAIL,
            'sender_name': request.user.username,
        })

        try:
            send_mail(
                subject,
                text_message,
                settings.DEFAULT_FROM_EMAIL,  # Using the email address from settings
                [useremail],
                fail_silently=False,  # Do not fail silently, raise exceptions on errors
                html_message=html_message  # The HTML content
            )
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return render(request, 'invclc/admin_acess.html')