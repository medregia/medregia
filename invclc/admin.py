from django.contrib import admin
from .models import Invoice,DeletedInvoice,ModifiedInvoice
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin

class adminInvoice(admin.ModelAdmin):
	list_display= ['user','pharmacy_name', 'invoice_number', 'invoice_date','balance_amount', 'payment_amount']
	# history_list_display = ["pharmacy_name"]

class AdminDeletedInvoice(admin.ModelAdmin):
    list_display = ['today_date','pharmacy','payment','balance']
    
class AdminModifiedInvoice(admin.ModelAdmin):
    list_display = ['modified_today_date','modified_pharmacy','modified_payment','modified_balance']
    
admin.site.register(Invoice, adminInvoice)
admin.site.register(DeletedInvoice,AdminDeletedInvoice)
admin.site.register(ModifiedInvoice,AdminModifiedInvoice)
