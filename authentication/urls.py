from .views import UserViews ,LoginViews , RegisterViews , LogoutViews , UserActionViews
from django.urls import path 

urlpatterns = [
    path("" , UserViews.as_view()),
    path("login",LoginViews.as_view()),
    path("register",RegisterViews.as_view()),
    path("logout",LogoutViews.as_view()),
    path("user",UserActionViews.as_view()),
    path("user/<str:pk>",UserActionViews.as_view())
]