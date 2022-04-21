from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.loginUserView, name='loginUser'),
    path('register/', views.registerUserView, name='registerUser'),
    path('logout/', views.logoutUserView, name='logoutUser'),
    path('profile/', views.profileUserView, name='profileUser'),
    path('updateProfile/', views.updateProfileView, name='updateProfile')
]