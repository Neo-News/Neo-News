import os
import boto3
import requests
from boto3.session import Session
from datetime import datetime

from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth import login

from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
from .models import ProfileImage, User
from .exception import SocialLoginException, KakaoException

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
        login(request, user)
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

# 일단 signup.html 렌더링 하려고 만든 클래스
class UserSignupView(View):

    def get(self, request, **kwargs):
      return render(request, 'signup.html')


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
    
