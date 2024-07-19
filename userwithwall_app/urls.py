from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.index),
    path('register' , views.register),
    path('wall' , views.success),
    path('logout' , views.logout),
    path('login' , views.validate_login),
    path('new_message' , views.create_message),
    path('create_comment' , views.create_comment),
    path("clear_comment" , views.clear_comment)
]



