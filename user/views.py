from django.shortcuts import render
from django.views.generic import View


class SignupDeatilView(View):
  def get(self,request, *args, **kwargs):
    return render(request, 'signup_detail.html')

  def post(self, *args, **kwargs):
    pass