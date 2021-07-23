from os import name
from django.urls import path

from django.contrib.auth.views import LogoutView
from user.views import (
    UserLoginView, UserSignupView, SignupDeatilView, UserInforEditView, ImageUpload,
    Activate, UserInforAddView, kakao_login, kakao_login_callback, ChangePasswordView,
    DeletePasswordView)



app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/kakao/', kakao_login, name='kakao-login'),
    path('login/social/kakao/callback/', kakao_login_callback, name='kakao-callback'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('signup/', UserSignupView.as_view(), name='signup'),
    path('account/activate/<str:uidb64>/<str:token>/', Activate.as_view()),
    path('signup/detail/', SignupDeatilView.as_view() ,name='signup_detail'),
    path('infor/', UserInforAddView.as_view(), name='infor'),
    path('infor/edit/', UserInforEditView.as_view() ,name='infor-edit'),
    path('password/', ChangePasswordView.as_view(), name='change_password'),
    path('infor/image/', ImageUpload, name='image-upload'),
    path('delete/', DeletePasswordView.as_view(), name='delete'),
]
