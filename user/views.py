from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
import boto3
from boto3.session import Session
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
from datetime import datetime
from .models import ProfileImage

class UserLoginView(LoginView):
    template_name = 'login.html'
    
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
    
