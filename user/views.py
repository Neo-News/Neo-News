from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView

class SignupDeatilView(View):
  def get(self,request, *args, **kwargs):
    return render(request, 'signup_detail.html')

  def post(self, *args, **kwargs):
    pass


class UserLoginView(LoginView):
    template_name = 'login.html'
    

class UserInforEditView(View):

    def get(self, request, **kwargs):
      return render(request, 'user-infor-edit.html')
