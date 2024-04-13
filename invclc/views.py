from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice,DeletedInvoice,ModifiedInvoice,TrackingPayment
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
from django.core.serializers import serialize

# views.py
from django.http import JsonResponse
from .models import Invoice


def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith(('.csv')):
                try:
                    csv_data = file.read().decode('utf-8').splitlines()
                    csv_reader = csv.DictReader(csv_data)
                    
                    # Assuming you have a way to get the current user (e.g., request.user)
                    current_user = request.user
                    
                    for row in csv_reader:
                        # Convert date string to datetime object
                        invoice_date = datetime.strptime(row['invoice_date'], '%d/%m/%Y').date()
                        
                        # Convert string values to integers
                        invoice_amount = int(row['invoice_amount'])
                        payment_amount = int(row['payment_amount'])
                        
                        # Calculate balance amount
                        balance_amount = invoice_amount - payment_amount
                        
                        # Get the current date and time
                        current_date = datetime.now().date()
                        current_time = datetime.now().time()
                        
                        # Create Invoice object for each row in the CSV file
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

                    
                    return JsonResponse({'message': 'CSV content uploaded successfully'})
                except Exception as e:
                    return JsonResponse({'error': f'Error processing CSV file: {str(e)}'}, status=500)
            else:
                return JsonResponse({'error': 'File format not supported. Please upload a CSV file.'}, status=400)
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='/')
def exports_to_csv(request):
    check_user = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                        print("check_user : ",check_user)
                except Exception as a:
                    print("Collaborating Error : ", a)
    except Exception as e:
        print("Error : ", e)
    
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
            print ("Exception : ",e)
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
            print("Exception : ",a)


def exports_to_xlsx(request):   
    check_user = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                        print("check_user : ",check_user)
                except Exception as a:
                    print("Collaborating Error : ", a)
    except Exception as e:
        print("Error : ", e)
        
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
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                        print("check_user : ",check_user)
                except Exception as a:
                    print("Collaborating Error : ", a)
    except Exception as e:
        print("Error : ", e)
        
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
    payment_details = invoices.filter().order_by('-id')
    q_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    search_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), Q(payment_amount=0))
    payed_details = invoices.filter(balance_amount=0.00).order_by('-id')
    check_user = None
    check_admin= None
    unique_code_id = None
    try:
        unique_code = Person.objects.get(user = request.user)
        unique_id = unique_code.UniqueId
    except Person.DoesNotExist:
        unique_code =f"'{request.user}' Please Update Your Profile"
        unique_id = f"'{request.user}' Please Update Your Profile"

    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                        # Use filter instead of get
                        check_admin = Invoice.objects.filter(user=collaborator_admin).first()
                        unique_code_id = Person.objects.get(user=collaborator_admin)
                        print("User name : ", check_user)
                        print("unique code :", unique_code_id.UniqueId)
                        print("REQUEST TYPE", request.user.username)
                except Exception as a:
                    print("Collaborating Error : ", a)
                print(f"Collaborate username: {collaborator_sender_username}")
                print(f"Admin username: {current_user.username if current_user else None}")

    except Exception as e:
        print("Error When Collaborating the User", e)


    if str(request.user) == check_user:
        DeleteHistory = DeletedInvoice.objects.filter(user=collaborator_admin).order_by('-id')
    else:
        DeleteHistory = DeletedInvoice.objects.filter(user=request.user).order_by('-id')
        
    if not DeleteHistory.exists():
        DeleteHistory = "No Deletion Found"
        
    if str(request.user) == check_user:
        ModifiedHistory = ModifiedInvoice.objects.filter(user = collaborator_admin).order_by('-id')
    else:
        ModifiedHistory = ModifiedInvoice.objects.filter(user = request.user).order_by('-id')
        
    if not ModifiedHistory.exists():
        ModifiedHistory = "No Updatation Found"
        
    Storename = None
    admin_invoices = None
    try:
        if check_user == str(request.user): 
            Storename = Person.objects.get(user=collaborator_admin)
            print("Store Type : ",Storename)
        else:
            print("Using request.user")
            Storename = Person.objects.get(user=request.user)

        modifiedStore = convert_Medical(Storename.MedicalShopName)
        print(Storename.MedicalShopName)
    except Person.DoesNotExist:
        modifiedStore = "Not Found"


    try:
        if check_user == str(request.user): 
            Medicalname = Person.objects.get(user=collaborator_admin)
        else:
            Medicalname = Person.objects.get(user=current_user)
    except Person.DoesNotExist:
        Medicalname = ''
        
    full_paid =None
    edit_paid = None
    partially_paid = None
    debt_paid = None
    delete_history = None
    modified_history = None
    if check_user == str(request.user):
        admin_invoices = Invoice.objects.filter(user=collaborator_admin)
        full_paid = admin_invoices.filter(balance_amount=0.00).order_by('-id')
        edit_paid = admin_invoices.filter().order_by('-id')
        partially_paid = admin_invoices.filter(~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
        debt_paid = admin_invoices.filter(~Q(balance_amount=0.00), Q(payment_amount=0))
        
        # delete_history = DeletedInvoice.objects.filter(user=collaborator_admin).order_by('-id')
        # if not delete_history.exists():
        #     delete_history = "No Deletion Found"
            
        # modified_history = ModifiedInvoice.objects.filter(user = collaborator_admin).order_by('-id')
        # if not modified_history.exists():
        #     modified_history = "No Updatation Found"
            
        if full_paid.exists():
            print("payment :", full_paid)
        else:
            print("No fully paid invoices found for the collaborator admin.", collaborator_admin)
    else:
        print("Current user is not a collaborator admin.")


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
            if check_user == str(request.user):
                invoice = invoice_form.save(commit=False)
                invoice.user = collaborator_admin
            else:
                invoice = invoice_form.save(commit=False)
                invoice.user = request.user
            invoice.updated_by = request.user

            # Save the Invoice object
            invoice.save()

            # Calculate the updated payment amount

            # Create and save TrackingPayment instance
            tracking_payment = TrackingPayment(
                user=invoice.user,
                Medical_name=invoice.pharmacy_name,
                Medical_payments=invoice.invoice_amount,
                payment_date=invoice.today_date,
                paying_amount=invoice.payment_amount
            )
            tracking_payment.save()

            messages.success(request, " Payment Success")
            return redirect("index")
        else:
            messages.error(request, "Failed to save Invoice Number want to Unique ")

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
               'medicalname':Medicalname,
               'MedicalStatus':modifiedStore,
               'check_user':check_user,
               'check_admin':check_admin,
               'unique':unique_code_id,
               'current_user':str(request.user),
            #    'admin_storename':Storename.MedicalShopName,
               'admin_invoice':admin_invoices,
               'full_paid':full_paid,
               'edit_paid':edit_paid,
               'partially_paid':partially_paid,
               'debt_paid':debt_paid,
               'coloborate_delete':delete_history,
               'colloborate_modified':modified_history,
               #    'convert_Medical': convert_Medical,
               }
    return render(request,'invclc/index.html',context)

def convert_Medical(shopname):
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
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    print("Collaborating Error : ", a)
            
    except Exception as e:
        print("Something Wrong in 540 ", e)
        
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
    upload_csv_file = UploadFileForm
    check_user = None
    data = None
    admin_city = None  # Initialize admin_city variable
    admin_ph = None
    admin_uniqueid = None
    admin_person = None
    user_city =None
    user_ph =None
    unique_id = None
    collaborator_admin = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                        print("check_user : ",check_user)
                except Exception as a:
                    print("Collaborating Error : ", a)
    except Exception as e:
        print("Error : ", e)
    
    if str(request.user) == check_user:        
        try:
            person = Person.objects.get(user=collaborator_admin)
            print("Person : ", person)
            city = person.City
            print("City", city)
            unique_id = person.UniqueId
            admin_person = person.user.username
            print(admin_person)
            admin_city = person.City
            get_admin_ph = CustomUser.objects.get(username=collaborator_admin) 
            admin_ph = get_admin_ph.phone_num
            admin_uniqueid = person.UniqueId
            
            user = Person.objects.get(user=request.user)
            print("User : ", user)
            user_city = user.City
            print(user_city)
            get_user_ph = CustomUser.objects.get(username=request.user)
            user_ph = get_user_ph.phone_num 
            unique_id = user.UniqueId
            
            data = Invoice.objects.filter(user=collaborator_admin).order_by('id')
        except Exception as a:
            print("Exception : ",a)
    else:        
        try:
            user = Person.objects.get(user=request.user)
            print("User : ", user)
            user_city = user.City
            print(user_city)
            get_user_ph = CustomUser.objects.get(username=request.user)
            user_ph = get_user_ph.phone_num 
            unique_id = user.UniqueId
            data = Invoice.objects.filter(user=request.user).order_by('id')
        except Exception as e:
            print("Current User : ",e)
        
    user_name = request.user
    if request.method == 'POST':
        completed = request.POST.get('completed', False)
        category = request.POST.get('category', '')  # Get category as comma-separated string
        others = request.POST.get('others', False)
        print(others)
        # Split category string into a list
        category_list = category.split(',')

        # Here, you would filter your data based on the parameters received and return the filtered data.
        # Replace the code below with your actual data filtering logic.
        # Example filtering logic:
        data = Invoice.objects.all()  # Assuming YourModel is your model name
        if completed:
            data = data.filter(balance_amount = 0,user=request.user)
            print("user data : ",data)
        if category_list:
            print(category_list)
            users_with_category = CustomUser.objects.filter(store_type__in=category_list)
            # Iterate over each user in the queryset to access their username
            for user in users_with_category:
                print("Category User : ", user.username)
            data = data.filter(user__in=users_with_category)
        else:
            print("Hii")
       # You can add more filters based on 'others' if needed
       # Render the filtered data to the template
    
    context = {
        'datas': data,
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
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    print("Collaborating Error : ", a)
            
    except Exception as e:
        print("Something Wrong in 540 ", e)
    
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
    collaborator_admin = None
    
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    print("Collaborating Error : ", a)
            
    except Exception as e:
        print("Something Wrong in 540 ", e)
    if collaborator_admin and collaborator_admin is not None:
        invoices = Invoice.objects.filter(Q(user=collaborator_admin ), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    else:
        invoices = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount'))).order_by('-id')
    return render(request, 'invclc/paymore.html',{'invoices': invoices})

@login_required(login_url='/')
def updatemore_view(request):
    current_user = request.user
    check_user = None 
    collaborator_admin = None
    try:
        collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    print("Collaborating Error : ", a)
            
    except Exception as e:
        print("Something Wrong in 540 ", e)
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
        print(f"Number of collaborator requests found: {collaborator_requests.count()}")
        
        for notification in collaborator_requests:
            collaborator_request_username = notification.sender.username
            get_admin_name = notification.receiver.username
            print('Get_Admin_name', get_admin_name)
            print(f"Collaborator request sender username: {collaborator_request_username}")
            
            collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
            collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
            print("collaborator_admin : ", collaborator_admin)
            print("new : ", collaborator_request_sender)
            
            for user in collaborator_request_sender:
                collaborator_sender_username = user.username
                try:
                    current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                    if current_user and collaborator_admin:
                        check_user = current_user.username
                except Exception as a:
                    print("Collaborating Error : ", a)
            
    except Exception as e:
        print("Something Wrong in 540 ", e)
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
        invoice.invoice_amount = Decimal(data.get('invoice_amount', invoice.invoice_amount))
        invoice.invoice_date = data.get('invoice_date', invoice.invoice_date)
        invoice.balance_amount = Decimal(data.get('balance_amount', invoice.balance_amount))

        # Perform the necessary conversions
        invoice_date = data.get('invoice_date', invoice.invoice_date)
        invoice_date = parse_date(invoice_date)

        # Update the invoice_date field
        invoice.invoice_date = invoice_date

        # Update the payment_amount based on the balance_amount
        invoice.payment_amount = invoice.invoice_amount - invoice.balance_amount

        # Save the updated Invoice
        invoice.save()
        
        check_user = None  # Define check_user here
        
        try:
            collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
            print(f"Number of collaborator requests found: {collaborator_requests.count()}")
            
            for notification in collaborator_requests:
                collaborator_request_username = notification.sender.username
                get_admin_name = notification.receiver.username
                print('Get_Admin_name', get_admin_name)
                print(f"Collaborator request sender username: {collaborator_request_username}")
                
                collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
                collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
                print("collaborator_admin : ", collaborator_admin)
                print("new : ", collaborator_request_sender)
                
                for user in collaborator_request_sender:
                    collaborator_sender_username = user.username
                    try:
                        current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                        if current_user and collaborator_admin:
                            check_user = current_user.username
                    except Exception as a:
                        print("Collaborating Error : ", a)
                
        except Exception as e:
            print("Something Wrong in 540 ", e)
            
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
        
        check_user = None  # Define check_user here
        
        try:
            collaborator_requests = Notification.objects.filter(sender=request.user, is_read=True)
            print(f"Number of collaborator requests found: {collaborator_requests.count()}")
            
            for notification in collaborator_requests:
                collaborator_request_username = notification.sender.username
                get_admin_name = notification.receiver.username
                print('Get_Admin_name', get_admin_name)
                print(f"Collaborator request sender username: {collaborator_request_username}")
                
                collaborator_request_sender = CustomUser.objects.filter(username=collaborator_request_username, is_staff=False)
                collaborator_admin = CustomUser.objects.get(username=get_admin_name, is_staff=True)
                print("collaborator_admin : ", collaborator_admin)
                print("new : ", collaborator_request_sender)
                
                for user in collaborator_request_sender:
                    collaborator_sender_username = user.username
                    try:
                        current_user = CustomUser.objects.get(username=collaborator_sender_username, is_staff=False)
                        if current_user and collaborator_admin:
                            check_user = current_user.username
                    except Exception as a:
                        print("Collaborating Error : ", a)
                
        except Exception as e:
            print("Something Wrong in 540 ", e)

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
        
        tracking_payment = TrackingPayment(
            user=invoice.user,
            Medical_name = invoice.pharmacy_name,
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
        print("Error",e)
        messages.error(request,"Payment Falied")
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
        
        tracking_payment = TrackingPayment(
            user=invoice.user,
            Medical_name = invoice.pharmacy_name,
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
