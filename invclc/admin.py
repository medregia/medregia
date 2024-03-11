from django.contrib import admin
from .models import Invoice
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin

# class adminInvoice(SimpleHistoryAdmin):
# 	list_display= ['user','pharmacy_name', 'invoice_number', 'invoice_date','balance_amount', 'payment_amount']
	# history_list_display = ["pharmacy_name"]

admin.site.register(Invoice, ImportExportModelAdmin)

