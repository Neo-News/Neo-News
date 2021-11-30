from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    UserLoginView, UserSignupView, SignupDeatilView, ChangeMyInforView,
    SignupRedirectView, kakao_login, kakao_login_callback, ChangePasswordView,
    DeletePasswordView, FindPwView, FindPasswordEmailView, AuthNumConfirmView,
    ValidChangePwdView, LoginCallBackView, ResendEmailView,
    UserKeywordDeleteView, UserKeywordEditView, UserCategoryEditView, 
    MypageView, LikeArticleView, CommentArticleView, UserInforAddView
    )

app_name = 'user'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('account/activate/<str:uidb64>/<str:token>/', SignupRedirectView.as_view()),
    path('signup/re/email/', ResendEmailView.as_view(), name='resend'),
    path('signup/detail/', SignupDeatilView.as_view() ,name='signup_detail'),
    
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/kakao/', kakao_login, name='kakao-login'),
    path('login/social/kakao/callback/', kakao_login_callback, name='kakao-callback'),
    path('login/callback/', LoginCallBackView.as_view(), name='login_callback'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('password/',FindPwView.as_view(), name='password'),

    path('password/check/',FindPasswordEmailView.as_view(), name='password_check'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('password/valid/change/', ValidChangePwdView.as_view(), name='valid_change_pwd'),
    path('password/confirm/', AuthNumConfirmView.as_view(), name='confirm_password'),
    path('delete/', DeletePasswordView.as_view(), name='delete'),
    
    path('infor/', UserInforAddView.as_view(), name='infor'),
    path('infor/category/', UserCategoryEditView.as_view() ,name='category_infor'),
    path('infor/change/', ChangeMyInforView.as_view(), name='change-infor'),
    
    path('keyword/delete/', UserKeywordDeleteView.as_view() ,name='keyword_delete'),
    path('keyword/create/', UserKeywordEditView.as_view() ,name='keyword_create'),
    
    path('mypage/', MypageView.as_view(), name='mypage'),
    path('like/article/', LikeArticleView.as_view(), name='like-article'),
    path('comment/article/', CommentArticleView.as_view(), name='comment-article'),
]

