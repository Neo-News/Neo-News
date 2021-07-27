from utils import context_infor
from user.dto import SignupDto
from user.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from user.text import message, pwd_change_message

import jwt

class UserService():
  
  @staticmethod
  def create(dto:SignupDto):
    """
    user 생성
    """
    user = User.objects.create_user(
    email = dto.email,
    nickname = dto.nickname,
    password = dto.password,
      )
    return user

  @staticmethod
  def verify_email_user(request, pk, email):
    """
    이메일 입력한 유저의 이메일 인증 데이터 리턴
    """
    current_site = get_current_site(request)
    domain = current_site.domain
    uidb64 = urlsafe_base64_encode(force_bytes(pk))
    token = jwt.encode({'user_pk' : pk}, 'secretkey', algorithm = 'HS256').decode('utf-8')
    message_data = message(domain, uidb64, token)
    mail_title = '이메일 인증을 완료해주세요'
    data ={'email': email}  
    mail_to = data['email']
    return (mail_title, message_data, mail_to)

  @staticmethod
  def verify_pwd_user(request, pk, email, auth_num):
    """
    (비밀번호 변경)이메일 입력한 유저의 이메일 인증 데이터 리턴
    """
    message_data = pwd_change_message(auth_num)
    mail_title = '이메일 인증을 완료해주세요'
    data = context_infor(email=email)  
    mail_to = data['email']
    return (mail_title, message_data, mail_to)

  @staticmethod
  def get_by_user(pk):
    user = User.objects.get(pk=pk)
    return user

  @staticmethod
  def verify_user_active(user,user_pk, token):
    """
    유저의 pk와 token에 담겨있는 유저의 pk같을 경우
    is_active=True로 변경
    """
    if user_pk == token:
        user.is_active = True
        user.save()
        return True
    else:
        return False

  @staticmethod
  def update(pk,dto,recent_email):
    
    User.objects.filter(email=recent_email).update(
      email = dto.email
    )
    user = User.objects.filter(email=dto.email).first()
    print('skurseouroier',user)
    return user

  def update_nickname(request, nickname):
    User.objects.filter(pk=request.user.pk).update(
      nickname=nickname
    )
    user = User.objects.filter(pk=request.user.pk).first()
    return user
