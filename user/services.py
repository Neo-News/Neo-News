import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import check_password

from config.settings import SECRET_KEY, ALGORITHM

from utils import context_info
from user.dto import SignupDto, UserDto, VaildEmailDto, UserConfirmDto
from user.text import message, pwd_change_message
from user.tasks import send_email
from user.models import User


class UserService():
  
    @staticmethod
    def create(dto:SignupDto):

        return User.objects.create_user(
                    email = dto.email,
                    nickname = dto.nickname,
                    password = dto.password,
                    )

    @staticmethod
    def get_user(pk):
        return User.objects.get(pk=pk)

    @staticmethod
    def get_user_like(user):
        return user.like.all()

    @staticmethod
    def get_email_user(value):
        return User.objects.filter(email=value).first()

    @staticmethod
    def get_filter_auth_user(dto:UserConfirmDto):
        return User.objects.get(email=dto.email, auth=dto.valid_num)

    @staticmethod
    def update(email, resend_email):
        User.objects.filter(email=email).update(email=resend_email)
        return User.objects.get(email=resend_email)

    @staticmethod
    def update_nickname(request, nickname):
        User.objects.filter(pk=request.user.pk).update(nickname=nickname)
        user = User.objects.filter(pk=request.user.pk).first()
        return user

    @staticmethod
    def update_active(pk):
        return User.objects.filter(pk=pk).update(is_active=False)

    @staticmethod
    def vaildate_user_password(dto:UserDto):
        if dto.password == '':
            error = True
            msg = '비밀번호를 입력해주세요 !'
            context = context_info(error=error, msg=msg)
            return context

        if not check_password(dto.password, dto.password_chk):
            error = True
            msg = '비밀번호를 틀렸어요 !'
            context = context_info(error=error, msg=msg)
            return context

    @staticmethod
    def vaildate_user_email(dto:VaildEmailDto):
        if not dto.email:
            msg = '이메일을 입력해주세요'
            context = context_info(error=True, msg=msg)   

            return context     

        user = UserService.get_email_user(dto.email)

        if not user:
            msg = '존재하지 않는 이메일이에요'
            context = context_info(error=True, msg=msg)

            return context

        return context_info(error=False, user=user)


class UserEmailVerifyService():
    @staticmethod
    def send_email_with_auth_num(email, auth_num):
        message_data = pwd_change_message(auth_num)
        mail_title = '이메일 인증을 완료해주세요'
        mail_to = email
        send_email.delay(mail_title, message_data, mail_to)
        
        context = context_info(
        msg='이메일에 인증번호를 발송했습니다!', 
        error=False, 
        auth_num=auth_num
        )

        return context
    
    @staticmethod
    def user_email(request, pk, email):  
        domain = get_current_site(request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(pk))
        token = jwt.encode({'user_pk' : pk}, SECRET_KEY, ALGORITHM).decode('utf-8')

        message_data = message(domain, uidb64, token)
        mail_title = '이메일 인증을 완료해주세요'
        mail_to = email
        
        return (mail_title, message_data, mail_to)


    @staticmethod
    def verify_user_active(user, token):
        if user.pk == token:
            user.is_active = True
            user.save()

    @staticmethod
    def verify_num(dto:UserConfirmDto):
        if not User.objects.filter(email=dto.email, auth=dto.valid_num).exists():
            msg = '인증번호가 올바르지 않습니다. 인증번호를 다시한번 확인해주세요 !'
            context = context_info(success=False, msg=msg) 
            
            return context
        
        context = context_info(success=True)     
        
        return context
    
    @staticmethod
    def verify_change_pwd(form, current_user):
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            current_user.set_password(new_password)
            current_user.save()
            context=context_info(error=False, url='https://neonews.site/user/login/callback/')
            
            return context

        error = form.non_field_errors()
        context = context_info(msg=error, error=True)
        
        return context      
