from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import StateModel, DistrictModel, Person,MakeUsAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_num', 'store_type','other_value','is_staff')
    search_fields = ('username','phone_num','email','pin','store_type','other_value')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('phone_num','pin','store_type','other_value'),
        }),
    )

class StateModelAdmin(admin.ModelAdmin):
    model:StateModel
    list_display =[
        'Pid',
        'Pname',
    ]
class DistrictModelAdmin(admin.ModelAdmin):
    model:DistrictModel
    list_display =[
        'Pid',
        'districtname',
    ]

class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = [
            'user',
            'MedicalShopName',
            'ProprietaryName',
            'UniqueId',
        ]
    
class CreateAdmin(admin.ModelAdmin):
    model = MakeUsAdmin
    list_display = ('newAdmin','date_joined')
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StateModel,StateModelAdmin)
admin.site.register(DistrictModel,DistrictModelAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(MakeUsAdmin,CreateAdmin)