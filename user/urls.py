from django.urls import path

from django.contrib.auth.views import LogoutView
from user.views import UserLoginView, UserSignupView, SignupDeatilView, UserInforEditView, ImageUpload, Activate, UserInforAddView, kakao_login, kakao_login_callback



app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/kakao/', kakao_login, name='kakao-login'),
    path('login/social/kakao/callback/', kakao_login_callback, name='kakao-callback'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signup/detail/', SignupDeatilView.as_view() ,name='signup_detail'),
    path('infor/edit/', UserInforEditView.as_view() ,name='infor-edit'),
    path('infor/image/', ImageUpload, name='image-upload'),
    path('account/activate/<str:uidb64>/<str:token>/', Activate.as_view()),
    path('infor/edit/image/', ImageUpload, name='image-upload'),
    path('account/activate/<str:uidb64>/<str:token>/', Activate.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),

]
