from django.contrib.auth.models import User
from authentication.models import Notification,CustomUser

def admin_info(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {'admin_user': request.user}
    else:
        return {}


def nav_message(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        # Query notifications where the current user is the receiver
        notifications = Notification.objects.filter(receiver=current_user, is_read=False,falied_request=False)
    else:
        # If the user is not authenticated, return an empty list of notifications
        notifications = []
    
    return {'notifications': notifications}