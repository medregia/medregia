from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from .forms import SignUpForm
from django.shortcuts import render, redirect
from .models import CustomUser,Person,Notification
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .profile import ProfileForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import views as auth_views
from invclc.models import Invoice,DeletedInvoice,ModifiedInvoice,TrackingPayment
import json 
from .models import StateModel, DistrictModel,ConnectMedicals,RegisterMedicals
from django.http import HttpResponse,JsonResponse
from .UniqueCode import User_code
from authentication.forms import InsensitiveAuthentication
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .context_processors import nav_message
from django.template.loader import render_to_string
from django.db.utils import IntegrityError
from django import forms
from decimal import Decimal
import traceback
from .service import SendNotification
import os 


def admin_page(request):
    return redirect('/admin/')

def signup_view(request):
    try:
        form = SignUpForm()
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True  # Grant staff status to new users
                store_type = form.cleaned_data.get('store_type')
                if store_type == 'other':
                    other_value = form.cleaned_data.get('other_value')
                    user.other_value = other_value
                user.save()

                # Create a group for the user (optional)
                user_group, created = Group.objects.get_or_create(name="Admin Group")
                
                deleted_invoice_content_type = ContentType.objects.get_for_model(DeletedInvoice)
                
                view_deleted_invoice_permission = Permission.objects.get(codename='view_deletedinvoice')
                delete_deleted_invoice_permission = Permission.objects.get(codename='delete_deletedinvoice')
                
                user_group.permissions.add(view_deleted_invoice_permission)
                user_group.permissions.add(delete_deleted_invoice_permission)
                
                

                # Get the content type for the Invoice model
                invoice_content_type = ContentType.objects.get_for_model(Invoice)
                
                add_invoice_permission = Permission.objects.get(codename='add_invoice')
                view_invoice_permission = Permission.objects.get(codename='view_invoice')
                change_invoice_permission = Permission.objects.get(codename='change_invoice')
                delete_invoice_permission = Permission.objects.get(codename='delete_invoice')
                
                user_group.permissions.add(add_invoice_permission)
                user_group.permissions.add(view_invoice_permission)
                user_group.permissions.add(change_invoice_permission)
                user_group.permissions.add(delete_invoice_permission)
                
                
                modified_invoice_content_type = ContentType.objects.get_for_model(ModifiedInvoice)
                
                # Define permissions for ModifiedInvoice model
                view_modified_invoice_permission = Permission.objects.get(codename='view_modifiedinvoice')
                delete_modified_invoice_permission = Permission.objects.get(codename='delete_modifiedinvoice')
                
                # Add permissions for ModifiedInvoice model to the group
                user_group.permissions.add(view_modified_invoice_permission)
                user_group.permissions.add(delete_modified_invoice_permission)


                # Get the content type for the TrackingPayment model
                tracking_payment_content_type = ContentType.objects.get_for_model(TrackingPayment)
                
                # Define permissions for TrackingPayment model
                view_tracking_payment_permission = Permission.objects.get(codename='view_trackingpayment')
                delete_tracking_payment_permission = Permission.objects.get(codename='delete_trackingpayment')
                
                # Add permissions for TrackingPayment model to the group
                user_group.permissions.add(view_tracking_payment_permission)
                user_group.permissions.add(delete_tracking_payment_permission)
                # Assign the user to the group
                user.groups.add(user_group)
                user.save()
                
                try:
                    subject = 'Welcome to MedRegia!'
                    message = render_to_string('authentication/welcome_email.html', {'user': user})
                    email_from = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [user.email]
                    send_mail(subject, message, email_from, recipient_list)
                except Exception as email_error:
                    messages.warning(request, "Signup successful, but failed to send the welcome email.")
                
                messages.success(request, "Signup successful")
                return redirect("/")
    except Exception as e:
        print("Error in Signup : ",e)
    return render(request, 'authentication/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        login_form = InsensitiveAuthentication(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('index/')

    else:
        login_form = InsensitiveAuthentication(request)
        login_form.fields['username'].widget.attrs.update({'placeholder': 'Username','autocomplete':'off'})
        login_form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        
    return render(request, 'authentication/login.html', {'form': login_form})


def phone_login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_num = data.get('phone_num')
        pin = data.get('pin')
        
        if phone_num and pin:
            try: 
                user = CustomUser.objects.get(phone_num=phone_num, pin=int(pin))
                login(request, user)
                return JsonResponse({'message': 'Logged in'}, status=200)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Invalid Username or PIN'}, status=400)
            except CustomUser.MultipleObjectsReturned:
                logout(request)
                return JsonResponse({'error': 'Phone Number Already Taken'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
    
    return render(request, 'authentication/phonelogin.html')
    

@login_required(login_url='/')
def profile_view(request):
    checked_username = None
    BASE_DIR = settings.BASE_DIR

    try:
        # Load and process states data
        with open(os.path.join(BASE_DIR, 'india_locations.json'), 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                if item['LocationType'] == 'State':
                    StateModel.objects.get_or_create(
                        Pid=item['Pid'],
                        LocationType=item['LocationType'],
                        Pname=item['Pname']
                    )

        # Load and process districts data
        with open(os.path.join(BASE_DIR, 'india_district.json'), 'r') as json_file:
            district_data = json.load(json_file)
            for items in district_data:
                if items['LocationType'] == 'District':
                    state_instance = StateModel.objects.get(Pid=items['Pid'])
                    # Check if the district already exists, if not, create it
                    DistrictModel.objects.get_or_create(
                        id=items['ID'],
                        Pid=items['Pid'],
                        LocationType=items['LocationType'],
                        districtname=items['districtname'],
                        state=state_instance
                    )

    except FileNotFoundError:
        print("JSON file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    permissions = Permission.objects.filter(content_type__model='invoice')

    current_user = request.user
    profile_data = CustomUser.objects.get(username=current_user)
    district_data = DistrictModel.objects.all()

    profile, created = Person.objects.get_or_create(user=current_user)

    user_data = User_code(profile)
    profile.UniqueId = user_data.display()
    profile.save()

    try:
        # Notifications handling
        read_notifications = Notification.objects.filter(receiver=request.user, is_read=True)
        for notification in read_notifications:
            sender_username = notification.sender.username
            receiver_username = notification.receiver.username
            staff_senders = CustomUser.objects.filter(username=sender_username, is_staff=True)
            if staff_senders.exists():
                normal_user = CustomUser.objects.get(username=receiver_username, is_staff=False)
                for user in staff_senders:  
                    sender_name = user.username
                    try:
                        CustomUser.objects.get(username=sender_name, is_staff=True)
                        receiver_name = CustomUser.objects.get(username=normal_user.username, is_staff=False)
                        if receiver_name:
                            checked_username = receiver_name.username
                    except CustomUser.DoesNotExist as user_error:
                        messages.error(request, user_error)

    except Exception as general_error:  
        messages.error(request, f"Something went wrong while exporting JSON: {general_error}")

    if request.method == "POST":
        data = json.loads(request.body)
        check_person = Person.objects.get(user=request.user)

        errors = []
        fields_to_check = ['ProprietaryNumber', 'ProprietaryContact', 'DrugLiceneseNumber2', 'DrugLiceneseNumber1','RegisteredNumber']
        
        for field in fields_to_check:
            if data.get(field):
                existing_profile = Person.objects.filter(**{field: data.get(field)}).exclude(user=request.user).first()
                if existing_profile:
                    errors.append(f"{field} '{data.get(field)}' already exists in another record.")
                else:
                    setattr(profile, field, data.get(field))

        state_id = data.get('state')
        district_id = data.get('district')
        districtKey = data.get('districtkey')

        if state_id:
            state_instance = StateModel.objects.get(Pid=state_id)
            profile.state = state_instance

        if district_id and districtKey:
            try:
                district_instance = DistrictModel.objects.get(Pid=district_id, id=districtKey)
                profile.district = district_instance
            except DistrictModel.DoesNotExist:
                messages.error(request, "DistrictModel with the provided districtKey does not exist.")

        checked = True
        if not errors:
            profile.save()
            if checked:
                check_medical_register = RegisterMedicals.objects.filter(
                    Medical_name=data.get('MedicalShopName'),
                    # dl_number1=data.get('DrugLiceneseNumber1'),
                    # dl_number2=data.get('DrugLiceneseNumber2')
                ).first()

                if check_medical_register and profile.MedicalShopName == check_medical_register.Medical_name:
                    return JsonResponse({
                        'success': True,
                        'dl1': f'{check_medical_register.dl_number1}',
                        'dl2': f'{check_medical_register.dl_number2}',
                        'sender': check_medical_register.user.username  # Use a serializable field
                    }, status=200)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'errors': errors}, status=400)

    checked = False



    # Admin Data Logic
    existing_admin = Notification.objects.filter(receiver=request.user, is_read=True, request_status=True).first()
    admin_data = CustomUser.objects.get(username=existing_admin.sender if existing_admin else request.user)

    context = {
        'hide_colaborator': Notification.objects.filter(receiver=request.user, is_read=True, request_status=True).exists(),
        'user_profile_data': profile_data,
        'district_data': district_data,
        'unique_code': profile.UniqueId,
        'data': profile,
        'admin_name': admin_data.username,
        'admin_ph': admin_data.phone_num,
        'admin_position': admin_data.position,
        'sendShopName': profile_data.other_value and profile_data.other_value.capitalize() if profile_data.store_type == "others" else profile_data.store_type and profile_data.store_type.capitalize() ,
        'colaborator': Notification.objects.filter(sender=checked_username if checked_username == str(request.user) else request.user, is_read=True)
    }

    return render(request, 'authentication/profile.html', context)



def logout_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # Clear all messages.
            messages.set_level(request, messages.SUCCESS)
            while messages.get_messages(request):
                pass
            
            logout(request)
            messages.success(request, "Logout Successful")
        return redirect('login')
    else:
        return HttpResponseNotAllowed(['GET'])

@login_required(login_url='/')
def change_pin(request):
    if request.method == 'POST':
        User_request = request.user
        current_pin = int(request.POST.get('current_pin'))
        new_pin = request.POST.get('new_pin')
        confirm_new_pin = request.POST.get('confirm_new_pin')
        
        if current_pin == User_request.pin:
            if new_pin == confirm_new_pin:
                request.user.pin = new_pin
                request.user.save()

                messages.success(request, 'PIN changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Your PIN was not Match ..')
                
        else:
            messages.error(request, 'Invalid current PIN. Please try again.')

    return render(request, 'authentication/change_pin.html')


def get_districts(request, state_id=None,district_id = None):
    if state_id is None:
        state_id = request.GET.get('state')
    if district_id is None:
        district_id = request.GET.get('district_id')
        # print(district_id)
    

    if state_id is not None:
        districts = DistrictModel.objects.filter(state_id=state_id)
        district_list = [{'Pid': district.Pid, 'districtname': district.districtname,'id':district.id} for district in districts]
        return JsonResponse(district_list, safe=False)
    else:
        return JsonResponse({'error': 'State ID is required'}, status=400)

def get_states(request):
    states = StateModel.objects.all()
    state_list = [{'Pid': state.Pid, 'Pname': state.Pname} for state in states]
    return JsonResponse(state_list, safe=False)

@login_required(login_url='/')
def confirm_admin(request, uniqueid):
    try:
        sender_uniqueId = Person.objects.get(UniqueId=uniqueid)
        receiver_Medical = Person.objects.get(user=request.user)

        get_selected_invoice = Invoice.objects.filter(user=sender_uniqueId.user, pharmacy_name=receiver_Medical.MedicalShopName)
        sender_username = CustomUser.objects.get(username = sender_uniqueId.user)
        receiver_username = CustomUser.objects.get(username= request.user)


        if sender_uniqueId and get_selected_invoice.exists():
            for idx, selected_invoice in enumerate(get_selected_invoice):

                # Ensure the fields are not None before creating a new Invoice object
                invoice_amount = selected_invoice.invoice_amount if selected_invoice.invoice_amount is not None else Decimal('0.00')
                balance_amount = selected_invoice.balance_amount if selected_invoice.balance_amount is not None else Decimal('0.00')
                payment_amount = selected_invoice.payment_amount if selected_invoice.payment_amount is not None else Decimal('0.00')
                
                # Check if the invoice already exists for the current user
                invoice_exists = Invoice.objects.filter(
                    user=request.user,
                    pharmacy_name=sender_uniqueId.MedicalShopName,
                    invoice_number=selected_invoice.invoice_number,
                    invoice_date=selected_invoice.invoice_date,
                    invoice_amount=invoice_amount,
                    balance_amount=balance_amount,
                    payment_amount=payment_amount,
                    today_date=selected_invoice.today_date,
                    current_time=selected_invoice.current_time,
                    updated_by=selected_invoice.updated_by
                ).exists()
                
                if invoice_exists:
                    continue  # Skip if the invoice already exists
                
                selected_invoice.collaborator_invoice = receiver_username
                selected_invoice.save()
                
                # Create a new Invoice object
                Invoice.objects.create(
                    user=request.user,
                    pharmacy_name=sender_uniqueId.MedicalShopName,
                    invoice_number=selected_invoice.invoice_number,
                    invoice_date=selected_invoice.invoice_date,
                    invoice_amount=invoice_amount,
                    balance_amount=balance_amount,
                    payment_amount=payment_amount,
                    today_date=selected_invoice.today_date,
                    current_time=selected_invoice.current_time,
                    updated_by=selected_invoice.updated_by,
                    collaborator_invoice = sender_username,
                )
                
            messages.success(request, f"Collaboration Success with {sender_uniqueId.user.username}")
        else:
            messages.error(request, "No Invoice Found in this Name")

        notification_message = f"{request.user} Accepted the Request "
        # Update the ConnectMedicals object to mark it as read
        get_ConnectMedicals = ConnectMedicals.objects.get(request_receiver=request.user,request_sender = sender_uniqueId.user, is_read=False, accept_status=True)
        # print("get_ConnectMedicals : ",get_ConnectMedicals)
        get_ConnectMedicals.is_read = True
        get_ConnectMedicals.request_message = notification_message
        get_ConnectMedicals.status_message = "Request Accepted"
        get_ConnectMedicals.save()

    except Person.DoesNotExist:
        messages.error(request, f"Person with UniqueId {uniqueid} does not exist.")
    except Invoice.DoesNotExist:
        messages.error(request, "Invoice does not exist for the logged-in user.")
    except Exception as e:
        print("Error :",e)
        messages.error(request, f"An error occurred: {e}")
    
    return redirect('index')

@login_required(login_url='/')
def admin_cancel(request,uniqueid):
    # print("uniqueid : ",uniqueid)
    try:
        get_sender_name = Person.objects.get(UniqueId = uniqueid)
        reject_message = f"{request.user} Reject the Colloboration Request "
        notification = get_object_or_404(ConnectMedicals, request_receiver=request.user, request_sender = get_sender_name.user, is_read=False, accept_status=True)
        notification.is_read = True
        notification.accept_status = False
        notification.request_message = reject_message
        notification.status_message = "Request Rejected"
        notification.save()

        messages.info(request,"coloboration Canceled")
        return redirect('index')
    except Exception as e:
        return messages.error(request,"Somthing Wrong in Admin Cancel Request",e)
        
@login_required(login_url='/')
def colaborator_list(request):
    try:
        colaborator = Notification.objects.filter(receiver=request.user)
    except Exception as a:
        colaborator = None
        
    return render(request,'authentication/colaborator.html',{'colaborator':colaborator})

@login_required(login_url='/login/')
def clinic_page(request):
    return render(request, 'authentication/clinic.html')
    
@login_required(login_url='/login/')
def all_notification(request):  # Ensure this function is present
    return render(request, 'authentication/all_notification.html')