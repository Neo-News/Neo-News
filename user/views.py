
import os
import jwt
import json
import requests
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import logout, authenticate, login as auth_login
from django.views.generic import View, FormView, TemplateView
from django.http.response import JsonResponse
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

from boto3.session import Session
from config.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME,
    SECRET_KEY, ALGORITHM
    
    )

from utils import context_info, email_auth_num
from user.dto import (
    AuthDto, SignupDto, ResendDto,
    UserDto, UserPkDto, VaildEmailDto, UserConfirmDto
    )
from user.forms import (
    FindPwForm, SignupForm, LoginForm, 
    ChangeSetPwdForm,VerificationEmailForm
    )
from news.dto import KeywordInforDto, KeywordDto, CategoryDto
from user.mixin import VerifyEmailMixin
from user.models import User, Category, Keyword
from news.models import UserPress
from user.services import UserService, UserEmailVerifyService
from news.services import CategoryService, KeyWordsService, PressService
from user.exception import SocialLoginException, KakaoException
from social.services import CommentService


class UserSignupView(VerifyEmailMixin, View):

    def get(self, request, *args, **kwargs):
        forms = SignupForm()
        context = context_info(forms=forms)

        return render(request, 'signup.html', context)
  
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            signup_form = SignupForm(json.loads(request.body))
            data = self._build_signup_dto(request)

            form_info = self.verify_form(signup_form)
            
            if form_info["error"]:
                return JsonResponse(form_info)

            mail_info = self.verify_email(data)
            
            context = self.send_user_email(request, mail_info)

            return JsonResponse(context)

    def _build_signup_dto(self, request):
        data = json.loads(request.body)
        return SignupDto(
            email = data['email'],
            nickname = data['nickname'],
            password = data['password']
        )
        

class SignupRedirectView(View):
    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserService.get_user(uid)
        token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        
        UserEmailVerifyService.verify_user_active(user, token['user_pk'])
        
        return redirect('user:login')


class SignupDeatilView(LoginRequiredMixin,View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self,request, *args, **kwargs):
        categories = CategoryService.get_exclude_categories('속보')

        context = context_info(categories=categories)
        
        return render(request, 'signup_detail.html', context)


class ResendEmailView(VerifyEmailMixin, View):
    def get(self, request, *args, **kwargs):
        forms = VerificationEmailForm()
        forms = str(forms)
        
        context = context_info(forms=forms)
        
        return JsonResponse(context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._build_resend_dto(request)
            resend_signup_form = VerificationEmailForm(json.loads(request.body))

            form_info = self.verify_form(resend_signup_form)
            
            if form_info["error"]:
                return JsonResponse(form_info)

            mail_info = self.verify_resend_email(data)
            
            if mail_info["error"]:
                return JsonResponse(mail_info)

            context = self.send_user_email(request, mail_info)

            return JsonResponse(context)

    def _build_resend_dto(self, request):
        data = json.loads(request.body)
        return ResendDto(
            resend_email = data['resend-email'],
            email = data['email']
        )


class UserLoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'
    
    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            auth_login(self.request, user)

        if User.objects.filter(pk=self.request.user.pk).first().is_detailed == False:
            categories = Category.objects.all()
            context = context_info(categories=categories)
            return render(self.request,'signup_detail.html',context)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.' )
        return super().form_invalid(form)

# 카카오 로그인 뷰
def kakao_login(request):
    try:
        if request.user.is_authenticated:
            raise SocialLoginException("User arleady logged in")

        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = "https://neonews.site/user/login/social/kakao/callback/"
    
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
        )
    
    except KakaoException as error:
        messages.error(request, error)
        return redirect("index")

    except SocialLoginException as error:
        messages.error(request, error)
        return redirect("index")


# 카카오 로그인 콜백뷰
def kakao_login_callback(request):
    try: 
        if request.user.is_authenticated:
            raise SocialLoginException("User arleady logged in")
        code = request.GET.get("code", None)  # code = authorization_code
        if code is None:
            KakaoException("Can't get code")

        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = "https://neonews.site/user/login/social/kakao/callback/"
        client_secret = os.environ.get("KAKAO_SECRET_KEY")
        request_access_token = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}",
            headers={"Accept": "application/json"},
        )
        token_info_json = request_access_token.json()
        error = token_info_json.get("error", None)
        if error is not None:
            KakaoException("Can't get access token")

        access_token = token_info_json.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers=headers,
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")

        nickname = profile.get("nickname", None)
        email = kakao_account.get("email", None)

        user, created = User.objects.get_or_create(email=email)
        if created:
          user.set_password(None)
          user.nickname = nickname
          user.is_active = True
          user.save()
          auth_login(request, user)
          return redirect("user:signup_detail")
        
        auth_login(request, user)
        return redirect("index")

    except KakaoException as error:
        messages.error(request, error)
        return redirect("index")

    except SocialLoginException as error:
        messages.error(request, error)
        return redirect("index")


class ChangeMyInforView(View):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            file = request.FILES.get('img')
            if file:
                session = Session(
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_S3_REGION_NAME
                )

                s3 = session.resource('s3')
                now = datetime.now().strftime('%Y%H%M%S')
                img_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
                    Key = now+file.name,
                    Body = file
                )
                s3_url = "https://neonews-s3.s3.ap-northeast-2.amazonaws.com/"
                User.objects.filter(pk=request.user.pk).update(
                    image=s3_url+now+file.name
                )
                
            nickname = request.POST['infor-user-nickname']
            if nickname:
                User.objects.filter(pk=request.user.pk).update(
                    nickname=nickname
                )
            user = User.objects.filter(pk=request.user.pk).first()
            context = {
                'user' : user,
                'msg' : {
                    'state' : True,
                    'text' : '개인정보가 변경되었습니다.'
                }
            }
            return render(request, 'user-infor.html', context)    


class UserKeywordEditView(LoginRequiredMixin,View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = self._build_keyword_dto(request)
            keyword = KeyWordsService.get_keyword_name(data.keyword)

            if not keyword:
                keyword = KeyWordsService.create(data.keyword)

            keyword.users.add(data.user)
            context = context_info(keyword_pk=keyword.pk, content=keyword.name)
            return JsonResponse(context)

    def _build_keyword_dto(self, request):
        data = json.loads(request.body)
        return KeywordInforDto(
            keyword = data.get('todo'),
            user = request.user
        )
            

class UserKeywordDeleteView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = self._build_keyword_dto(request)
            keyword = KeyWordsService.get_keyword(data.keyword_pk)

            if keyword :
                keyword.users.remove(request.user)

            context = context_info(is_completed=True)
            return JsonResponse(context)

    def _build_keyword_dto(self, request):
        data = json.loads(request.body)
        return KeywordDto(
            keyword_pk = data.get('keyword_pk'),
            user_pk = request.user.pk
        )


class UserCategoryEditView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = self._build_category_dto(request)
            category = CategoryService.get_category_name(data.category_pk
            )
            CategoryService.get_filter_category_users(request, category)
            categories = CategoryService.get_filter_categories(data.user_pk)
            category_list = [category.name for category in categories]
            context = context_info(category_list=category_list)
            return JsonResponse(context)
    
    def _build_category_dto(self, request):
        data = json.loads(request.body)
        return CategoryDto(
            user_pk = request.user.pk,
            category_pk = data.get('category_pk')
        )

class UserInforAddView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = '/'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)

            for category in data.get('category_list'):
                CategoryService.filter_category_name(category).users.add(request.user)

            for keyword in data.get('todo_list'):
                if not KeyWordsService.get_keyword_name(keyword):
                    Keyword.objects.create(name=keyword)

                KeyWordsService.get_keyword_name(keyword).users.add(request.user)
            
            user = User.objects.get(pk=data['user_pk'])
            user.is_detailed = True
            user.save()

            presses = PressService.get_presses()
            userpress = UserPress.objects.create(user=user)

            [userpress.press.add(press) for press in presses]
            
            return JsonResponse({
                'success':True,
                'url': 'https://neonews.site/'
                })


class ChangePasswordView(LoginRequiredMixin ,View):
    login_url = '/user/login/'
    redirect_field_name='/'
    
    def get(self, request, **kwargs):
        return render(request,'change-password.html')

    def post(self, request, **kwargs):
        session_user = request.session['auth']
        current_user = User.objects.get(email=session_user)
        auth_login(request, current_user)
        return redirect('/')


class DeletePasswordView(LoginRequiredMixin ,View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def post(self, request, **kwargs):
        if request.is_ajax():
            error = False
            data = self._build_user_dto(request)
            result = UserService.vaildate_user_password(data)
            if result['error']:
                return JsonResponse(result)
            
            UserService.update_active(data.user_pk)
            logout(request)
            messages.success(request, '회원탈퇴 완료 !')
            context = context_info(error=error, url='https://neonews.site/')
            return JsonResponse(context)

    def _build_user_dto(self, request):
        data = json.loads(request.body)
        return UserDto(
            password=data.get('password'),
            password_chk=request.user.password,
            user_pk=request.user.pk
        )


class FindPwView(View):
    template_name = 'find_pw.html'
    find_pw = FindPwForm

    def get(self, request):
        form = self.find_pw(None)
        context = context_info(form=form)
        return render(request, self.template_name, context)


class FindPasswordEmailView(View):
    '''
    description: 비밀번호 찾으려는 유저의 이메일 유효성 검증, 검증 후 인증번호 이메일로 발송
    '''
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._build_vaild_email(request)
            result = UserService.vaildate_user_email(data)

            if result['error']:
                return JsonResponse(result)

            auth_num = email_auth_num()

            result['user'].auth = auth_num
            result['user'].save()

            context = UserEmailVerifyService.send_email_with_auth_num(data.email, auth_num)

            return JsonResponse(context)

    def _build_vaild_email(self, request):
        data = json.loads(request.body)

        return VaildEmailDto(
            email = data.get('email')
        )


class AuthNumConfirmView(View):
    '''
    description: 인증번호 유효성 검증, 검증 후 비밀번호 변경 view로 이동
    '''
    def get(self, request, *args, **kwargs):
        context = context_info(name=request.user.nickname)

        return render(request,'change-password.html',context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._build_user_confirm_info(request)
            result = UserEmailVerifyService.verify_num(data)

            if not result['success']:
                return JsonResponse(result)

            user = UserService.get_filter_auth_user(data)

            user.auth = ''
            user.save()

            request.session['auth'] = user.email
            context = context_info(result=user.email, success=True) 

            return JsonResponse(context)

    def _build_user_confirm_info(self, request):
        data = json.loads(request.body)

        return UserConfirmDto(
            email=data.get('email'),
            valid_num=data.get('valid_num')
        )


@method_decorator(csrf_exempt, name='dispatch') 
class ValidChangePwdView(View):
    '''
    description: 변경된 비밀번호 유효성 검증, 검증후 유저의 비밀번호 변경
    '''
    def get(self, request, *args, **kwargs):
        reset_pwd_form = ChangeSetPwdForm(None)
        context = context_info(forms=reset_pwd_form)

        return render(request, 'valid-change-pwd.html', context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._build_vaild_pwd_info(request)
            current_user = UserService.get_email_user(data.auth)
            
            auth_login(request, current_user)

            reset_pwd_form = ChangeSetPwdForm(current_user, json.loads(request.body))
            result = UserEmailVerifyService.verify_change_pwd(reset_pwd_form, current_user)
            
            return JsonResponse(result)

    def _build_vaild_pwd_info(self, request):
        return AuthDto(
            auth = request.session.get('auth'),
            user = request.user
        )


class LoginCallBackView(TemplateView):
    template_name = 'login_callback.html'

    def get(self, request, *args, **kwargs):
        context = {'message': 'SUCCESS'}
        return self.render_to_response(context)


class MypageView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self, request, **kwargs):
        data = self._build_user_info(request)
        user = UserService.get_user(data.pk)
        context = context_info(user=user)
        return render(request, 'user-infor.html', context)  

    def _build_user_info(self, request):
        return UserPkDto(
            pk = request.user.pk
        )


class LikeArticleView(LoginRequiredMixin, View):
    login_url = '/user/login/'    
    redirect_field_name='/'

    def get(self, request, **kwargs):
        data = self._build_user_info(request)
        user = UserService.get_user(data.pk)
        likes = UserService.get_user_like(user)
        context = context_info(likes=likes)
        return render(request, 'user-like.html', context)

    def _build_user_info(self, request):
        return UserPkDto(
            pk = request.user.pk
        )


class CommentArticleView(LoginRequiredMixin, View):
    login_url = '/user/login/'    
    redirect_field_name='/'

    def get(self, request, **kwargs):
        data = self._build_user_info(request)
        comments = CommentService.get_user_comment(data.pk)
        context = context_info(comments=comments)
        return render(request, 'user-comment.html', context)
    
    def _build_user_info(self, request):
        return UserPkDto(
            pk = request.user.pk
        )
