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
from .models import StateModel, DistrictModel
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

def signup_view(request):
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
            
            subject = 'Welcome to MedRegia !'
            message = render_to_string('authentication/welcome_email.html', {'user': user})
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, "Signup Success")
            return redirect("/")
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
        login_form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        login_form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        
    return render(request, 'authentication/login.html', {'form': login_form})


def phone_login_view(request):
    if request.user.is_authenticated:
        return redirect("index/")
    else:
        if request.method == "POST":
            phone_num = request.POST.get('phone_num', None)
            pin = request.POST.get('pin', None)
            if phone_num is not None and pin is not None:
                try: 
                    user = CustomUser.objects.get(phone_num=phone_num, pin=int(pin))
                except CustomUser.DoesNotExist:
                    messages.error(request, "Invalid UserName")
                    return redirect("/")
            if user is not None:
                login(request,user)
                messages.success(request, "logged in")
                return redirect("index/")
            else:
                messages.error(request, "Invalid UserName") 
                return redirect("/")
        return render(request, 'authentication/phonelogin.html')
    

@login_required(login_url='/')
def profile_view(request):
    BASE_DIR = settings.BASE_DIR
    try:
        with open(BASE_DIR / 'india_locations.json', 'r') as json_file:
            data = json.load(json_file)

        for item in data:
            if item['LocationType'] == 'State':
                state_instance, created = StateModel.objects.get_or_create(Pid=item['Pid'], LocationType=item['LocationType'], Pname=item['Pname'])

        with open(BASE_DIR / 'india_district.json', 'r') as json_file:
            district_data = json.load(json_file)

        for items in district_data:
            if items['LocationType'] == 'District':
                state_instance = StateModel.objects.get(Pid=items['Pid'])
                district_instance = DistrictModel.objects.filter(id=items['ID'],Pid=items['Pid'], LocationType=items['LocationType'], districtname=items['districtname']).first()
                if not district_instance:
                    district_instance = DistrictModel.objects.create(id=items['ID'],Pid=items['Pid'], LocationType=items['LocationType'], districtname=items['districtname'], state=state_instance)  # set the state field to the state instance

    except Exception as e:
        return messages.error(request,"Error State and District upload to Database",e)
        
    permissions = Permission.objects.filter(content_type__model='invoice')

    current_user = request.user
    profile_data = CustomUser.objects.get(username=current_user)
    district_data = DistrictModel.objects.all()

    profile , created =  Person.objects.get_or_create(user=current_user)

    user_data = User_code(profile)
    unique_id = user_data.display()

    profile.UniqueId = unique_id
    profile.save()
    existing_admin = None
    
    profile = Person.objects.get(user=current_user)
    
    if request.method == "POST": 
        data = json.loads(request.body)
        receiver_name = data.get('adminName',None)
        # print(data)
        try:
            if receiver_name is not None:
                receiver = CustomUser.objects.get(username=receiver_name)
                if receiver and receiver_name is not None:
                    if receiver == request.user:
                        response_data = {'message': 'Cannot Send Request to Yourself', 'adminName': receiver_name}
                        # return redirect("profile")
                        return JsonResponse({'error': response_data}, status=500)

                    # Check if the sender has already sent a request to the receiver
                    existing_request = Notification.objects.filter(sender=request.user, receiver=receiver).exists()
                    if existing_request:
                        response_data = {'message': 'You have already sent a request to this receiver', 'adminName': receiver_name}
                        # messages.error(request, f'You have already sent a request to this receiver {receiver_name}.')
                        # return redirect("profile")
                        return JsonResponse({'error': response_data}, status=500)

                    admin = Notification(sender=request.user, receiver=receiver, message="User Request")
                    admin.save()
                    response_data = {'message': 'Request successfully received', 'adminName': receiver_name}
                    return JsonResponse(response_data)

                else:   
                    response_data = {'message': 'Admin Request Not Sent', 'adminName': receiver_name}
                    # messages.error(request, "Admin Request Not Sent")
                    # return redirect("profile")
            else:
                response_data = {'message': 'Admin Request Not Sent', 'adminName': receiver_name}
                
            
                            
            check_person = Person.objects.get(user=request.user)
            if profile and check_person:
                errors = []       
                if check_person.MedicalShopName != '' and data.get('MedicalShopName'):
                    profile.MedicalShopName = data.get('MedicalShopName')  
                    
                if check_person.ProprietaryName != '' and data.get('ProprietaryName'):
                    existing_profile = Person.objects.filter(ProprietaryName=data.get('ProprietaryName')).exclude(user=request.user).first()
                    if existing_profile:
                        errors.append(f"ProprietaryName '{data.get('ProprietaryName')}' already exists in another record.")
                        # return JsonResponse({'errors': errors}, status=405)
                    else:
                        profile.ProprietaryName = data.get('ProprietaryName')  
                    
                if check_person.ProprietaryNumber != '' and data.get('ProprietaryNumber'):
                    existing_profile = Person.objects.filter(ProprietaryNumber=data.get('ProprietaryNumber')).exclude(user=request.user).first()
                    if existing_profile:
                        errors.append(f"ProprietaryNumber '{data.get('ProprietaryNumber')}' already exists in another record.")
                        # return JsonResponse({'errors': errors}, status=405)
                    else:
                        profile.ProprietaryNumber = data.get('ProprietaryNumber')  
                    
                if check_person.ProprietaryContact != '' and data.get('ProprietaryContact'):
                    existing_profile = Person.objects.filter(ProprietaryContact=data.get('ProprietaryContact')).exclude(user=request.user).first()
                    if existing_profile:
                        errors.append(f"ProprietaryContact '{data.get('ProprietaryContact')}' already exists in another record.")
                        # return JsonResponse({'errors': errors}, status=405)
                    else:
                        profile.ProprietaryContact = data.get('ProprietaryContact') 
                    
                if check_person.DrugLiceneseNumber2 != '' and data.get('DrugLiceneseNumber2'): 
                    existing_profile = Person.objects.filter(DrugLiceneseNumber2=data.get('DrugLiceneseNumber2')).exclude(user=request.user).first()
                    if existing_profile:
                        errors.append(f"DrugLiceneseNumber2 '{data.get('DrugLiceneseNumber2')}' already exists in another record.")
                        # return JsonResponse({'errors': errors}, status=405)
                    else:
                        profile.DrugLiceneseNumber2 = data.get('DrugLiceneseNumber2') 
                    
                if check_person.DrugLiceneseNumber1 != '' and data.get('DrugLiceneseNumber1') : 
                    existing_profile = Person.objects.filter(DrugLiceneseNumber1=data.get('DrugLiceneseNumber1')).exclude(user=request.user).first()
                    if existing_profile:
                        errors.append(f"DrugLiceneseNumber1 '{data.get('DrugLiceneseNumber1')}' already exists in another record.")
                        # return JsonResponse({'errors': errors}, status=405)
                    else:
                        profile.DrugLiceneseNumber1 = data.get('DrugLiceneseNumber1')  

                state_id = data.get('state')
                district_id = data.get('district')
                districtKey = data.get('districtkey')
                # print("districtKey : ",districtKey)
                # print(data)
                # print("State : ",state_id)
                # print("District : ",district_id)

                state_id = data.get('state')
                if check_person.state != '' and state_id:
                    state_instance = StateModel.objects.get(Pid=state_id)
                    # print("state_instance: ", state_instance)
                    profile.state = state_instance

                if district_id and districtKey:  # Check if both district_id and districtKey are present
                    try:
                        district_instance = DistrictModel.objects.get(Pid=district_id, id=districtKey)
                        # print("district_instance: ", district_instance)
                        profile.district = district_instance
                    except DistrictModel.DoesNotExist:
                        messages.error(request,"DistrictModel with the provided districtKey does not exist.")
                        
                if check_person.City != '' and data.get('City') :
                    profile.City = data.get('City')  
                
                if check_person.Pincode != '' and data.get('Pincode') : 
                    profile.Pincode = data.get('Pincode')  
                    
                if check_person.StreetNumber != '' and data.get('StreetNumber') :
                    profile.StreetNumber = data.get('StreetNumber')  
                    
                if check_person.DoorNumber != '' and data.get('DoorNumber') :
                    profile.DoorNumber = data.get('DoorNumber')  
                    
                if check_person.PharmacistName != '' and data.get('PharmacistName') : 
                    profile.PharmacistName = data.get('PharmacistName')
                    
                if check_person.RegisteredNumber != '' and data.get('RegisteredNumber') : 
                    existing_profile = Person.objects.filter(RegisteredNumber=data.get('RegisteredNumber')).exclude(user=request.user).first()
                    if existing_profile:
                        errors.append(f"RegisteredNumber '{data.get('RegisteredNumber')}' already exists in another record.")
                        # return JsonResponse({'errors': errors}, status=405)
                    else:
                        profile.RegisteredNumber = data.get('RegisteredNumber')
                  
                if check_person.ContactNumber != '' and data.get('ContactNumber') :     
                    profile.ContactNumber = data.get('ContactNumber') 
                     
                if check_person.PharmacistEmail != '' and data.get('PharmacistEmail') :     
                    profile.PharmacistEmail = data.get('PharmacistEmail')  

                # Assign the district_instance to a different field, assuming profile.district is the appropriate fiel
                if not errors:
                    profile.save()
                    return JsonResponse({'success': True})
                else:
                    # print(errors)
                    return JsonResponse({'errors': errors}, status=400)
                    
            else:
                return JsonResponse({'success': False})
        except CustomUser.DoesNotExist:
            response_data = {'message': 'No User Found with the username', 'adminName': receiver_name}
            return JsonResponse({'error': response_data}, status=500)
            # messages.error(request, f"No User Found with the username '{receiver_name}'")
        except IntegrityError as e:
            response_data = {'message': 'Request Already Sended', 'adminName': receiver_name}
            return JsonResponse({'error': response_data}, status=405)
            # messages.error(request, "Error: Duplicate entry for Drug License Number")
            # return redirect("profile") 

    
    existing_admin = Notification.objects.filter(sender=request.user,is_read=True, request_status=True)
    existing_admin_optional = Notification.objects.filter(sender=request.user,is_read=True, request_status=False)
    
    if existing_admin.exists():
        admin_data = CustomUser.objects.get(username=existing_admin.first().receiver)
        admin_name = admin_data.username
        admin_ph = admin_data.phone_num
        
    elif existing_admin_optional.exists():
        admin_data = CustomUser.objects.get(username=request.user)
        admin_name = admin_data.username
        admin_ph = admin_data.phone_num
    else:
        admin_data = CustomUser.objects.get(username=request.user)
        admin_name = admin_data.username
        admin_ph = admin_data.phone_num
        
    try:
        hide_colaborator = Notification.objects.filter(receiver=request.user, is_read=True, request_status=True).exists()
    except Notification.DoesNotExist:
        hide_colaborator = None

    get_shop_name = None
    sendShopName = None

    try:
        # Fetch the CustomUser instance for the current user
        userShopName = CustomUser.objects.get(username=request.user)
        
        # Extract values from the user instance
        get_shop_name = userShopName.store_type
        get_other_value = userShopName.other_value

        if get_shop_name and get_shop_name != "others":
            sendShopName = get_shop_name.capitalize()
            
        elif get_other_value and get_other_value != "store_type":
            sendShopName = get_other_value.capitalize()

    except CustomUser.DoesNotExist:
        userShopName = None
        sendShopName = None
    
        
    # Define the context dictionary
    context = {
        'hide_colaborator': hide_colaborator,
        'user_profile_data': profile_data,
        'district_data': district_data,
        'unique_code': profile.UniqueId, 
        'data': profile,
        'admin_name': admin_name,
        'admin_ph': admin_ph,
        'sendShopName': sendShopName,
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
def confirm_admin(request):
    collaborator_requests = Notification.objects.filter(receiver=request.user, is_read=False)
    admin_manager = CustomUser.objects.get(username=request.user)
    if collaborator_requests.exists():
        for collaborator in collaborator_requests:
            receiver = collaborator.receiver
            sender = collaborator.sender
            
            grand_accesses = Invoice.objects.filter(user__username=sender.username)
            
            if request.user.username == receiver.username:
                admin_group = Group.objects.get(name='Admin Group')
                sender.groups.remove(admin_group)
                sender.is_staff = False
                collaborator.is_read = True
                for grand_access in grand_accesses:
                    grand_access.user = receiver
                    grand_access.save()
                sender.save()
                collaborator.save()                
                messages.success(request, f"You have become a collaborator with {sender}.")
                request_user = CustomUser.objects.get(username=sender)
                
            else:
                messages.error(request, "You are not authorized to become an admin.")
    else:
        messages.error(request, "There are no pending collaborator requests.")
    
    return redirect('index')

@login_required(login_url='/')
def admin_cancel(request):
    try:
        notification = get_object_or_404(Notification, receiver=request.user, is_read=False, request_status=True)
        notification.request_status = False
        notification.save()
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


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    