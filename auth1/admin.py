from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from  django.contrib.auth.models  import  Group
from .models import RegisterUser, Notification

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'blood_group', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields =('email', 'username', 'blood_group')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

#my_models = [RegisterUser, AccountAdmin, Notification] # AccountAdmin

admin.site.register(RegisterUser, AccountAdmin)
admin.site.register(Notification)

# Remove group from admin panel
admin.site.unregister(Group)
