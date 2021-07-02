from django.urls import path
from user.views import SignupDeatilView

app_name = 'user'
urlpatterns = [
    path('signup/detail/', SignupDeatilView.as_view() ,name='signup_detail'),
]
