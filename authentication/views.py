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
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from .models import StateModel, DistrictModel
from django.http import HttpResponse,JsonResponse
from .UniqueCode import User_code
from .forms import LoginAuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .context_processors import nav_message

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

            messages.success(request, "Signup Success")
            return redirect("/")
    return render(request, 'authentication/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('index/')
    else:
        login_form = AuthenticationForm(request)
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
    

@login_required(login_url='/login/')
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
                district_instance = DistrictModel.objects.filter(Pid=items['Pid'], LocationType=items['LocationType'], districtname=items['districtname']).first()
                if not district_instance:
                    district_instance = DistrictModel.objects.create(Pid=items['Pid'], LocationType=items['LocationType'], districtname=items['districtname'], state=state_instance)  # set the state field to the state instance

    except Exception as e:
        print(f"Error: {e}")
        
    permissions = Permission.objects.filter(content_type__model='invoice')

    # Print permission codenames
    # for permission in permissions:
    #     print(permission.codename)

    current_user = request.user
    profile_data = CustomUser.objects.get(username=current_user)
    district_data = DistrictModel.objects.all()
    form = ProfileForm()

    profile , created =  Person.objects.get_or_create(user=current_user)

    user_data = User_code(profile)
    unique_id = user_data.display()
    # print(unique_id)

    profile.UniqueId = unique_id
    profile.save()

  
    profile = Person.objects.get(user=current_user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        receiver_name = request.POST.get('admin', None)
        try:
            receiver = CustomUser.objects.get(username=receiver_name)
            if receiver and receiver_name is not None:
                if receiver == request.user:
                    messages.error(request, f"Cannot Send Request to Yourself ({receiver_name})")
                    return redirect("profile")
                
                # Check if the sender has already sent a request to the receiver
                existing_request = Notification.objects.filter(sender=request.user, receiver=receiver).exists()
                if existing_request:
                    messages.error(request, f'You have already sent a request to this receiver {receiver_name}.')
                    return redirect("profile") 

                admin = Notification(sender=request.user, receiver=receiver, message="User Request")
                admin.save()
                messages.success(request, f"Collaborate Request Sent to User'{receiver}'")
                return redirect("index")

            else: 
                messages.error(request, "Admin Request Not Sent")
                return redirect("profile")
                
        except CustomUser.DoesNotExist:
            messages.error(request, f"No User Found with the username '{receiver_name}'")
            
        if form.is_valid():
            form.save()
            messages.success(request, "You Got It ")

        return redirect("profile")
        
    admins = CustomUser.objects.filter(is_staff=True).order_by('-date_joined')[:1]
    context = {
        'profile': form, 
        'user_profile_data': profile_data,
        'admins': admins, # sending Admin details
        'district_data': district_data,
        'unique_code':profile.UniqueId, 
        'data':profile,
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
        
        # print(f'current_pin: {current_pin}, type: {type(current_pin)}')
        # print(f'User_request.pin: {User_request.pin}, type: {type(User_request.pin)}')
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


def get_districts(request):
    state_id = request.GET.get('state')
    districts = DistrictModel.objects.filter(state_id=state_id)
    district_list = [{'id': d.id, 'name': d.districtname} for d in districts]
    return JsonResponse(district_list, safe=False)

@login_required(login_url='/')
def confirm_admin(request):
    collaborator_requests = Notification.objects.filter(receiver=request.user, is_read=False)
    if collaborator_requests.exists():
        # Assuming a user can have multiple pending collaborator requests
        for collaborator in collaborator_requests:
            receiver = collaborator.receiver
            sender = collaborator.sender
            # Check if the current user's username matches the new admin's username
            if request.user.username == receiver.username:
                admin_group = Group.objects.get(name='Admin Group')
                sender.groups.remove(admin_group)
                sender.is_staff = False
                collaborator.is_read = True
                sender.save()
                collaborator.save()
                messages.success(request, f"You have become a collaborator with {sender}.")
            else:
                messages.error(request, "You are not authorized to become an admin.")
    else:
        messages.error(request, "There are no pending collaborator requests.")
    
    return redirect('index')

@login_required(login_url='/')
def admin_cancel(request):
    try:
        notification = get_object_or_404(Notification, receiver=request.user, is_read=False, falied_request=False)
        notification.falied_request = True
        notification.save()
        return redirect('index')
    except Exception as e:
        print("Admin Cancel Error", e)

@login_required(login_url='/login/')
def clinic_page(request):
    return render(request, 'authentication/clinic.html')


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    