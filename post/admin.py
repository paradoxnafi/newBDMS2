from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import Post, Comment

# class PostAdmin(UserAdmin):
#     list_display = ('author', 'description', 'address', 'blood_group', 'required_bags', 'deadlineDate', 'deadlineTime', 'contact_number', 'created_at')
#     search_fields =('author', 'blood_group')
#     readonly_fields = ('author', 'created_at')

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

admin.site.register(Post)
admin.site.register(Comment)