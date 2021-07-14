import os
import boto3
import requests
from boto3.session import Session
from datetime import datetime

from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
from .models import ProfileImage, User
from .exception import SocialLoginException, KakaoException
from utils import context_infor
from user.forms import SignupForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.views.generic import View
from user.forms import SignupForm
from user.tasks import send_email
from user.services import UserService
from .dto import SignupDto
from django.contrib.auth import login as auth_login

import jwt
import json


class UserLoginView(LoginView):
    template_name = 'login.html'
    

# 카카오 로그인 뷰
def kakao_login(request):
    try:
        if request.user.is_authenticated:
            raise SocialLoginException("User arleady logged in")

        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = "http://127.0.0.1:8000/user/login/social/kakao/callback/"
    
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
        redirect_uri = "http://127.0.0.1:8000/user/login/social/kakao/callback/"
        client_secret = os.environ.get("KAKAO_SECRET_KEY")
        request_access_token = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}",
            headers={"Accept": "application/json"},
        )
        token_info_json = request_access_token.json()
        error = token_info_json.get("error", None)
        if error is not None:
            # print(error)
            KakaoException("Can't get access token")

        # print(token_info_json)
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

        user = User.objects.filter(email=email).first()
        print(user)
        if user is None:
            user = User.objects.create_user(
                email=email,
                nickname=nickname,
                image="default.png",
                password=None 
            )
            user.set_unusable_password()
            user.save()
        messages.success(request, f"{user.email} signed up and logged in with Kakao" )
        auth_login(request, user)
        return redirect(reverse("index"))

    except KakaoException as error:
        messages.error(request, error)
        return redirect("index")

    except SocialLoginException as error:
        messages.error(request, error)
        return redirect("index")

# user모델 생기면 수정 필요
# class UserSignupView(CreateView):
#     template_name = 'signup.html'


class UserSignupView(View):
  """
  author: Son Hee Jung
  date: 0713
  description: 
  회원의 정보를 ajax를 통해 받은 후 데이터를 form(modelformview)으로 보냄,
  formview에서는 데이터 폼에 대한 레이아웃 전송, 정보에 대한 유효성 검증 후 값 리턴
  검증이 끝난 데이터를 user model에 넣어준다. 이때 이메일에 대한 인증을 받기 위해 
  celery의 delay를 통해 비동기적으로 이메일 인증 받는다
  """

  def get(self, request, *args, **kwargs):
    """
    SignupForm을 통해 회원 폼 템플릿에 그려줌
    """
    forms = SignupForm()
    context = {'forms':forms}
    return render(request, 'signup.html',context)
  
  def post(self, request, *args, **kwargs):
    """
    ajax를 통해 회원 정보에 대한 유효성 검증과 유저의 모델을 생성
    """
    if request.is_ajax():
      data = json.loads(request.body)
      signup_form = SignupForm(data)

      if signup_form.is_valid():
        signup_data = self._build_signup_dto(signup_form)
        user = UserService.create(signup_data)
        mail_title, message_data, mail_to = UserService.verify_email_user(request, user.pk, signup_form.email)# 이메일 인증을 위한 데이터 변수들
        send_email.delay(mail_title, message_data, mail_to) # 이메일 인증을 위한 데이터 tasks로 따로 빼둠, 로딩 시간을 줄이기 위해 , 비동기 처리 (celery-redis기능) 
        context = context_infor(error='이메일을 인증해 회원가입을 완료하세요!', is_error=0)
        return JsonResponse(context)

      error = signup_form.non_field_errors()
      if error:
        context = context_infor(error=error, is_error=1)
        return JsonResponse(context) 
  
  @staticmethod
  def _build_signup_dto(data):
    return SignupDto(
      email = data.email,
      nickname = data.nickname,
      password = data.password
    )
        

class Activate(View):
    """
    author: Son Hee Jung
    date: 0713
    description: 
    유저 is_active change, jwt 토큰등 암호화 기능을 이용해서 이메일 인증에 필요한 데이터 생성
    """
    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserService.get_by_user(uid)
        token = jwt.decode(token,'secretkey',algorithm='HS256')
        result = UserService.verify_user_active(user,user.pk, token['user_pk'])
        auth_login(request, user)
        
        if result:
            return redirect('user:signup_detail')
        else:
            return redirect('user:signup_detail')


class SignupDeatilView(View):
  def get(self,request, *args, **kwargs):
    return render(request, 'signup_detail.html')

  def post(self, *args, **kwargs):
    pass


class UserInforEditView(View):

    def get(self, request, **kwargs):
        img = ProfileImage.objects.filter(pk=4).first()
        return render(request, 'user-infor-edit.html', {'img' : img})


# 프로필 이미지 등록하는 함수
def ImageUpload(request):
    if request.method == 'POST':
        file = request.FILES.get('img')
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
        ProfileImage.objects.create(
            title = now+file.name,
            url = s3_url+now+file.name
        )
        return redirect('user:infor-edit')

    # imgs = ProfileImage.objects.all()

    # return render(request, 'user-infor.html', {'imgs' : imgs})
    
