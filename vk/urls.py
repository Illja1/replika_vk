from django.urls import path
from . import views


urlpatterns = [
    path('',views.LoginPage,name='login'),
    path('logout/', views.Logout, name='logout'),
    path('create/', views.createProfile, name='profile'),
    path('register/', views.Singup, name='register'),
    path('main/', views.main, name='main'),
    path('upload/', views.upload_image, name='upload'),
    path('list/', views.user_list, name='list'),
    path('list_freind/', views.friend_user_list, name='f_list'),
    path('connect/<str:operation>/<int:pk>',views.change_friend,name='change'),
    path('add_news/',views.news_publish,name='pub'),
    path('news/',views.news_feed,name='all'),
    path('photo/',views.user_gallery,name='gallery'),
    path('news/<int:news_id>/like/', views.like_news, name='like_news'),
    path('msg/<int:recipient_id>', views.message, name='message'),
    path('msg_send/<str:recipient_id>', views.sendMessages, name='send_msg'),
    path('msg_rec/<str:recipient_id>', views.receiveMessages, name='rec_msg'),
    path('edit/', views.edit_profile, name='edit'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]
