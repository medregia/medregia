from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from .forms import SignUpForm
from django.contrib.auth.models import User 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from .forms import SignUpForm
from django.contrib.auth.models import User 
from .models import CustomUser,Person,MakeUsAdmin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .profile import ProfileForm,MakeAdmin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from invclc.models import Invoice
from invclc.forms import InvoiceForm
from django.db.models import Q
from django.db.models import F
import json 
import random
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from .models import StateModel, DistrictModel
from django.http import HttpResponse
from django.http import JsonResponse
from .UniqueCode import User_code


def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            store_type = form.cleaned_data.get('store_type')
            if store_type == 'other':
                other_value = form.cleaned_data.get('other_value')
                user.other_value = other_value
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
            print(login_form.errors)
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

    current_user = request.user
    profile_data = CustomUser.objects.filter(username=current_user)
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
        Admin_form = request.POST.get('admin', None)

        try:
            is_user = CustomUser.objects.get(username = Admin_form)
            if is_user and Admin_form is not None:
                admin = MakeUsAdmin(newAdmin = Admin_form)
                admin.save()
                messages.success(request, f"Admin Request Send to user '{Admin_form}'")
                return redirect("index")
            else: 
                messages.error(request,f"Admin Request Not sended")
                return redirect("profile")
                
        except CustomUser.DoesNotExist:
            messages.error(request, f"No User Found in This name {Admin_form}")

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
        'data':profile,    # use when you want data from Person Model
        
    }
    return render(request, 'authentication/profile.html', context)




def logout_view(request):

    if request.user.is_authenticated:
        # Clear all messages.
        messages.set_level(request, messages.SUCCESS)
        while messages.get_messages(request):
            pass
        
        logout(request)

        messages.success(request, "Logout Successful")
        return redirect('login')
    

# @login_required(login_url='/')
# def home_page(request):
#     current_user = request.user
#     query = request.POST.get('payment_list') if request.method == 'POST' else None
#     paied = request.POST.get('payed') if request.method == 'POST' else None
#     q = request.POST.get('q') if request.method == 'POST' else None
#     search = request.POST.get('search') if request.method == 'POST' else None

#     payment_details = Invoice.objects.filter(user=current_user)
#     payed_details = Invoice.objects.filter(user=current_user, balance_amount=0.00)
#     q_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), ~Q(balance_amount=F('invoice_amount')))
#     search_details = Invoice.objects.filter(Q(user=current_user), ~Q(balance_amount=0.00), Q(payment_amount=0))

#     if query is not None and query != 'all':
#         lookups = Q(pharmacy_name__icontains=query)
#         payment_details = payment_details.filter(lookups)
#     if paied is not None and paied != 'all':
#         search_payed = Q(pharmacy_name__icontains=paied)
#         payed_details = payed_details.filter(search_payed)
#     if q is not None and q != 'all':
#         q_payed = Q(pharmacy_name__icontains=q)
#         q_details = q_details.filter(q_payed)
#     if search is not None and search != 'all':
#         search_data = Q(pharmacy_name__icontains=search)
#         search_details = search_details.filter(search_data)

#     try:
#         person = Person.objects.get(user=request.user)
#         unique_id = person.UniqueId
#     except Person.DoesNotExist:
#         unique_id = "Please Update Your Profile"

#     invoice_form = InvoiceForm(request.POST if request.method == 'POST' else None)
#     if request.method == 'POST' and invoice_form.is_valid():
#         invoice = invoice_form.save(commit=False)
#         invoice.user = request.user
#         invoice.save()
#     elif request.method == 'POST':
#         messages.error(request, "This Invoice Number Already Exists..")

#     context = {
#         'form': invoice_form,
#         'payment': payment_details.order_by('-id'),
#         'payed_details': payed_details.order_by('-id'),
#         'q': q_details.order_by('-id'),
#         'search': search_details.order_by('-id'),
#         'unique': unique_id
#     }
#     return render(request, 'authentication/home.html', context)



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
     # Get the most recent MakeUsAdmin object
    current_admin = MakeUsAdmin.objects.order_by('-date_joined').first()

    # Check if the current user's username matches Admin_form
    if request.user.username == current_admin.newAdmin:
        # Demote the previous admin to a normal user
        previous_admin = CustomUser.objects.get(is_staff=True)
        if previous_admin:
            previous_admin.is_staff = False
            previous_admin.is_superuser = False
            previous_admin.save()

        # Make the current user an admin and a superuser
        request.user.is_staff = True
        request.user.is_superuser = True
        request.user.save()

        messages.success(request, "You are now an admin and a superuser.")
    else:
        messages.error(request, "You are not authorized to become an admin.")

    return redirect('index')

@login_required(login_url='/login/')
def payment_view(request):
    return render(request, 'authentication/index.html')

@login_required(login_url='/login/')
def clinic_page(request):
    return render(request, 'authentication/clinic.html')


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'