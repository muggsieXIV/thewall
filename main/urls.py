from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_create', views.process_create),
    path('process_login', views.process_login),
    path('welcome', views.welcome),
    path('logout', views.logout),
    path('process_message', views.process_message),
    path('comments', views.comments),
    path('process_comment', views.process_comment),
]