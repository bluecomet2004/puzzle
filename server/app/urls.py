from django.urls import path
from app.views import RegisterView, LoginView, TokenView, UserView, GameHistoryView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('token/', TokenView.as_view()),
    path('users/', UserView.as_view()),
    path('history/', GameHistoryView.as_view())
]
