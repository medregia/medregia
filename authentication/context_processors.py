from django.contrib.auth.models import User
from .models import MakeUsAdmin

def admin_info(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {'admin_user': request.user}
    else:
        return {}
    
def admin_form_data(request):
    current_admin = MakeUsAdmin.objects.order_by('-date_joined').first()
    if current_admin:
        Admin_form = current_admin.newAdmin
    else:
        Admin_form = None

    return {'Admin_form': Admin_form, 'admin_filter': current_admin}

