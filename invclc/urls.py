from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_invoice/<int:invoice_id>/', views.update_invoice, name='update_invoice'),
    path('delete_invoice/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('pay_invoice/<int:invoice_id>/', views.pay_invoice, name='pay_invoice'),
    path('payment_invoice/<int:payment_id>/', views.payment_invoice, name='payment_invoice'),
    # path('entry/',views.entrydata, name="entry"),
    path('update/', views.update_view, name='update'),
    path('delete/', views.delete_page, name='delete'),
    path('check/<int:id>', views.check_view, name='check'),
    path('statics/', views.staticspage_view, name='statics'),
    # path('create/', views.create_view, name='create'),
    path('update_view/<int:pk>/', views.update_view, name='update'),
    # path('payment/<int:payment_id>',views.payment_view, name="payment"),
    # path('edit/<int:id>',views.edit_view, name='edit'),
    # path('delete_view/<int:pk>/', views.delete_view, name='delete_view'),
    path('import-export/', views.import_view, name='import-export'),
    
    path('csv/', views.exports_to_csv, name='exports_to_csv'),
    path('xlsx/', views.exports_to_xlsx, name='exports_to_xlsx'),
    path('json/', views.exports_to_json, name='exports_to_json'),
    
    path('checkmore/', views.checkmore_view, name='checkmore'),
    path('paymore/', views.paymore_view, name='paymore'),
    path('updatemore/', views.updatemore_view, name='updatemore'),
    path('unpaid_debt/', views.unpaid_debt, name='unpaid_debt'),

    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('empty_csv/',views.empty_csv,name='empty_csv'),
    path('empty_xlsx/',views.empty_xlsx,name='empty_xlsx'),
    path('adminacess/',views.admin_access,name='adminacess'),
    path('invite/',views.invite_user,name='invite'),
    path('connect/',views.connect_view,name='connect'),
    path('create_medical/',views.create_medical_record,name="create_medical")
]