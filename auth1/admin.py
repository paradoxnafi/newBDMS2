from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from django import forms
from .models import RegisterUser, Notification

class AccountAdmin(ModelAdmin):
    list_display = ('email', 'username', 'blood_group', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields =('email', 'username', 'blood_group')
    readonly_fields = ('date_joined', 'last_login')
    exclude = ('password',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# class RegisterUserAdmin(forms.ModelForm):
#     class Meta:
#         model = RegisterUser
#         exclude = ['password']


admin.site.register(RegisterUser, AccountAdmin)
admin.site.register(Notification)

# Remove group from admin panel
admin.site.unregister(Group)
