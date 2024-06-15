from .models import ConnectMedicals

def send_notification(sender, recipient, message):
    ConnectMedicals.objects.create(request_sender=sender, request_receiver=recipient, request_message=message)