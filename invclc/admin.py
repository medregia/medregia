from django.contrib import admin
from .models import Invoice, DeletedInvoice, ModifiedInvoice,TrackingPayment,Invitation
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class AdminDeletedInvoice(admin.ModelAdmin):
    list_display = ['today_date', 'pharmacy', 'payment', 'balance']
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:
            # Superuser or staff user can see all invoices
            return queryset.filter(user=request.user)

class AdminModifiedInvoice(admin.ModelAdmin):
    list_display = ['modified_today_date', 'modified_pharmacy', 'modified_payment', 'modified_balance']
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:
            # Superuser or staff user can see all invoices
            return queryset.filter(user=request.user)
    
# class AdminInvoice(admin.ModelAdmin):
#     list_display = ['pharmacy_name', 'invoice_number', 'invoice_date', 'balance_amount', 'payment_amount']
    
class AdminTrackingPayments(admin.ModelAdmin):
    list_display = ['user', 'Medical_name', 'paying_amount', 'payment_date']
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:
            # Superuser or staff user can see all invoices
            return queryset.filter(user=request.user)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'pharmacy_name', 'invoice_date', 'invoice_amount')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:
            # Superuser or staff user can see all invoices
            return queryset.filter(user=request.user)
        
class InvitationAdmin(admin.ModelAdmin):
    list_display = [
        'mail_sendername','mail_receiver_name','mail_receiver_email','mail_receiver_phonenumber'
    ]
        
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(DeletedInvoice, AdminDeletedInvoice)
admin.site.register(ModifiedInvoice, AdminModifiedInvoice)
admin.site.register(TrackingPayment, AdminTrackingPayments)
admin.site.register(Invitation, InvitationAdmin)
