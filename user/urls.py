from os import name
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    UserLoginView, UserSignupView, SignupDeatilView, ImageUploadView,
    Activate, UserInforAddView, kakao_login, kakao_login_callback, ChangePasswordView,
    DeletePasswordView, FindPwView, PasswordCheckView, PasswordConfirmView,ValidChangePassword,
    LoginCallBackView, ResendEmailView,UserKeywordDeleteView,UserKeywordEditView,UserCategoryEditView, 
    MypageView, LikeArticleView, CommentArticleView)



app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/kakao/', kakao_login, name='kakao-login'),
    path('login/social/kakao/callback/', kakao_login_callback, name='kakao-callback'),
    path('login/callback/', LoginCallBackView.as_view(), name='login_callback'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/',FindPwView.as_view(), name='password'),
    path('password/check',PasswordCheckView.as_view(), name='password_check'),
    
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('account/activate/<str:uidb64>/<str:token>/', Activate.as_view()),
    path('signup/re/email/', ResendEmailView.as_view(), name='resend'),
    # path('password/activate/<str:uidb64>/<str:token>/', PwdActivate.as_view()),
    
    path('signup/detail/', SignupDeatilView.as_view() ,name='signup_detail'),
    path('infor/', UserInforAddView.as_view(), name='infor'),
    # path('infor/edit/', UserInforEditView.as_view() ,name='infor-edit'),
    path('infor/category/', UserCategoryEditView.as_view() ,name='category_infor'),
    path('keyword/delete/', UserKeywordDeleteView.as_view() ,name='keyword_delete'),
    path('keyword/create/', UserKeywordEditView.as_view() ,name='keyword_create'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('password/valid/change/', ValidChangePassword.as_view(), name='valid_change_pwd'),
    path('password/confirm/', PasswordConfirmView.as_view(), name='confirm_password'),
    path('delete/', DeletePasswordView.as_view(), name='delete'),

    path('mypage/', MypageView.as_view(), name='mypage'),
    path('infor/image/', ImageUploadView.as_view(), name='image-upload'),
    path('like/article/', LikeArticleView.as_view(), name='like-article'),
    path('comment/article/', CommentArticleView.as_view(), name='comment-article'),
]
