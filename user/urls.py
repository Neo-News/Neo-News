from django.urls import path

from user.views import UserLoginView, UserSignupView, SignupDeatilView, UserInforEditView

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signup/detail/', SignupDeatilView.as_view() ,name='signup_detail'),
    path('infor/edit/', UserInforEditView.as_view() ,name='infor-edit'),
]
