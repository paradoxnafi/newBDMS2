from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from .models import Post, Comment, Report

class PostAdmin(ModelAdmin):
    ordering = ('created_at',)
    list_display = ('author', 'blood_group', 'required_bags', 'contact_number', 'created_at', 'is_resolved', 'admin_approved')
    search_fields = ('author__name', 'blood_group', 'is_resolved',) # Can not add author as it is a foregin key to post
    readonly_fields = ('created_at',)
    exclude = ('password',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ReportAdmin(ModelAdmin):
    ordering = ('time_since',)
    list_display = ('time_since', 'download')
    search_fields = ('time_since',) # Can not add author as it is a foregin key to post
    readonly_fields = ()
    exclude = ('download',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Report,ReportAdmin)
