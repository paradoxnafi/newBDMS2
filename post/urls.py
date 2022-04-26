from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createpost/', views.createpost, name='createpost'),
    path('posts/view/<int:post_id>', views.single_post, name='single_post'),
    path('users/view/<int:user_id>', views.view_user, name='view_user'),
    path('posts/edit_post/<int:pk>', views.edit_post, name='edit_post'),
    path('posts/<int:pk>/delete/', views.delete_post, name="delete_post"),
    path('comments/<int:pk>/delete/', views.delete_comment, name="delete_comment"),
    path('posts/my_posts/', views.my_posts, name='my_posts'),
    path('generatePDF/', views.generatePDF, name='generatePDF'),
]