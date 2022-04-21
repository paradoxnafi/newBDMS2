from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createpost/', views.createpost, name='createpost'),
    # path("post/<int:pk>/", views.single_post, name="single-post"),
    path('posts/view/<int:post_id>',
         views.single_post, name='single_post'),
    path('users/view/<int:user_id>', views.view_user, name='view_user'),
]