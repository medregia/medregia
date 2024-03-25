from django.contrib import admin
from .models import Invoice, DeletedInvoice, ModifiedInvoice,TrackingPayment
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice
        fields = ['user', 'pharmacy_name', 'invoice_number', 'invoice_date', 'balance_amount', 'payment_amount']

class AdminDeletedInvoice(admin.ModelAdmin):
    list_display = ['today_date', 'pharmacy', 'payment', 'balance']

class AdminModifiedInvoice(admin.ModelAdmin):
    list_display = ['modified_today_date', 'modified_pharmacy', 'modified_payment', 'modified_balance']
    
class AdminInvoice(admin.ModelAdmin):
    list_display = ['pharmacy_name', 'invoice_number', 'invoice_date', 'balance_amount', 'payment_amount']
    
class AdminTrackingPayments(admin.ModelAdmin):
    list_display = ['user', 'Medical_name', 'Medical_payments', 'payment_date']

# class AdminInvoice(ImportExportModelAdmin):
#     resource_class = InvoiceResource

admin.site.register(Invoice, AdminInvoice)
admin.site.register(DeletedInvoice, AdminDeletedInvoice)
admin.site.register(ModifiedInvoice, AdminModifiedInvoice)
admin.site.register(TrackingPayment, AdminTrackingPayments)
