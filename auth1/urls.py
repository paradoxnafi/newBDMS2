from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.loginUserView, name='loginUser'),
    path('register/', views.registerUserView, name='registerUser'),
    path('logout/', views.logoutUserView, name='logoutUser'),
    path('profile/', views.profileUserView, name='profileUser'),
    path('updateProfile/', views.updateProfileView, name='updateProfile'),
    path('user/<int:pk>/notifications', views.view_notifications, name='view_notifications'),
    path('mark_as_read/<int:pk>', views.mark_as_read, name='mark_as_read'),
]