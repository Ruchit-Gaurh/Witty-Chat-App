from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('logout', views.logout, name='logout'),
    path('login', views.login_user, name='login'),
    path('login_page', views.login_page, name='login_page'),
    path('register_page', views.register_page, name='register_page'),
    path('register', views.register, name='register'),
    path('search_users/', views.search_users, name='search_users'),
    path('add_friend/<int:profile_id>/', views.add_friend, name='add_friend'), 
    path('<str:idf>', views.chat, name="chat"),
    path('loginkr/', views.loginkr, name='loginkr'),
    path('sent_msg/<str:idf>', views.sentMessage, name='sent_msg'),
    path('receive_msg/<str:idf>', views.receiveMessages, name='receive_msg'),
    path('sse_chat/<str:idf>', views.sse_chat_view, name='sse_chat'),
]