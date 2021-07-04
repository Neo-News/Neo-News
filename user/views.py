from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView


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
      return render(request, 'user-infor-edit.html')
