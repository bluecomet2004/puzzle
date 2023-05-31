from django.urls import path, include
from rest_framework import routers
from app.views import UserView, LoginView, GameHistoryView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('history/', GameHistoryView.as_view())
]
