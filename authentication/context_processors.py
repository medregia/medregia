from authentication.models import Notification,CustomUser,ConnectMedicals,RegisterMedicals
from authentication.models import Person
from django.contrib import messages

def admin_info(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {'admin_user': request.user}
    else:
        return {}


def nav_message(request):
    if request.user.is_authenticated:
        current_user = request.user
        notify_message = None
        incomplete_message = None
        sender_uniqueId = None
        
        notifications = ConnectMedicals.objects.filter(request_receiver=current_user, is_read=False, accept_status=True)
        
        try:
            
            collaborator_requests = ConnectMedicals.objects.filter(request_receiver=request.user, is_read=False).first()
            if collaborator_requests:
                get_sender_uniqueId = Person.objects.get(user=collaborator_requests.request_sender)
                if get_sender_uniqueId:
                    sender_uniqueId = get_sender_uniqueId.UniqueId
            
            if notifications.exists():
                check_profile = Person.objects.get(user=current_user)
                profile_uniqueId = check_profile.UniqueId

                if not profile_uniqueId or '####' in profile_uniqueId:
                    notify_message = True
                    if '####' in profile_uniqueId:
                        incomplete_message = "Your profile is still incomplete. Register the address section on your profile to access the request."
                else:
                    notify_message = False
                    
        except Person.DoesNotExist:
            messages.error(request, "No user found.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    else:
        # If the user is not authenticated, return empty values
        notifications = []
        notify_message = None
        incomplete_message = None
        sender_uniqueId = None
    
    return {
        'notifications': notifications,
        'notify_message': notify_message,
        'incomplete_message': incomplete_message,
        'sender_uniqueId': sender_uniqueId
    }

