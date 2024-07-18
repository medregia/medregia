from .models import ConnectMedicals

def SendNotification(sender, recipient, message,status):
    ConnectMedicals.objects.create(request_sender=sender, request_receiver=recipient, request_message=message,status_message = status)
