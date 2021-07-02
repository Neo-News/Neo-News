from django.urls import path

from user.views import SignupDeatilView
from user.views import UserLoginView

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/detail/', SignupDeatilView.as_view() ,name='signup_detail'),
]
