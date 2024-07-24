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
        timestamp = None
        accept_notification = None
        rejected_notification = None
        all_notifications = None
        get_MedicalName = None

        try:
            # Fetch notifications based on the current user's role
            notifications = ConnectMedicals.objects.filter(request_receiver=current_user, is_read=False, accept_status=True)
            
            collaborator_requests = ConnectMedicals.objects.filter(request_receiver=current_user, is_read=False).first()

            checked_notifications = ConnectMedicals.objects.filter(request_receiver=current_user, is_read=True, accept_status=True)
            failed_notifications = ConnectMedicals.objects.filter(request_receiver=current_user, is_read=True, accept_status=False)
            all_notifications = ConnectMedicals.objects.filter(request_receiver=current_user)
            
            get_MedicalName = Person.objects.get(user=current_user)

            if checked_notifications.exists():
                accept_notification = [accept.request_message for accept in checked_notifications]

            if failed_notifications.exists():
                rejected_notification = [failed.request_message for failed in failed_notifications]

            if collaborator_requests:
                get_sender_uniqueId = Person.objects.get(user=collaborator_requests.request_sender)
                if get_sender_uniqueId:
                    sender_uniqueId = get_sender_uniqueId.UniqueId
                    timestamp = collaborator_requests.timestamp

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
            # Handle cases where the Person object is not found
            messages.error(request, "User profile information not found.")
        except Exception as e:
            # Handle any other exceptions
            messages.error(request, f"An error occurred: {str(e)}")

    else:
        # Handle unauthenticated users
        notifications = []
        notify_message = None
        incomplete_message = None
        sender_uniqueId = None
        timestamp = None
        accept_notification = None
        rejected_notification = None
        all_notifications = None
        get_MedicalName = None

    return {
        'notifications': notifications,
        'notify_message': notify_message,
        'incomplete_message': incomplete_message,
        'sender_uniqueId': sender_uniqueId,
        'timestamp': timestamp,
        'accept_notification': accept_notification,
        'rejected_notification': rejected_notification,
        'all_notifications': all_notifications,
        'get_MedicalName': get_MedicalName.MedicalShopName if get_MedicalName else None,
    }


def all_notifications(request):
    all_notifications = None

    if request.user.is_authenticated:
        try:
            # Fetch notifications where the current user is the receiver
            receiver_notifications = ConnectMedicals.objects.filter(request_receiver=request.user)
            
            # Fetch notifications where the current user is the sender
            sender_notifications = ConnectMedicals.objects.filter(request_sender=request.user)
            
            # Combine both querysets
            all_notifications = sender_notifications | receiver_notifications
        except Exception as e:
            print("Error in All Notification:", e)
            all_notifications = None

    return {
        'all_notifications': all_notifications
    }


