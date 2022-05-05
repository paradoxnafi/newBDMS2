"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from post import views


admin.site.site_header  =  "Blood Donor Management System"  
admin.site.site_title  =  "Site Admin"
admin.site.index_title  =  "Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('auth1/', include('auth1.urls')),
]


handler404 = "auth1.views.handle_404"