from user.tasks import send_email
from user.services import UserService
from utils import context_infor
from user.models import User


class VerifyEmailMixin():
  def send_verification_email(self,request, signup_form, resent_email,change_email, email):
    if signup_form.is_valid():
      if email == 'new':
        signup_data = self._build_signup_dto(signup_form)
        user = UserService.create(signup_data)
        mail_title, message_data, mail_to = UserService.verify_email_user(request, user.pk, signup_form.email)# 이메일 인증을 위한 데이터 변수들
        send_email.delay(mail_title, message_data, mail_to) # 이메일 인증을 위한 데이터 tasks로 따로 빼둠, 로딩 시간을 줄이기 위해 , 비동기 처리 (celery-redis기능) 
        context = context_infor(
        msg='이메일을 인증해 회원가입을 완료하세요!',
          error=False
          )
        return context

      elif email == 'again':
        user = User.objects.filter(email = resent_email).first()
        another_user = User.objects.filter(email=change_email).first()
        if not user:
          context = context_infor(msg='회원가입부터 해주세요',error=True)
          return context
          
        if another_user and another_user != user:
          context = context_infor(msg='이미 회원가입된 이메일입니다. 다른 이메일을 입력해주세요', error=True)
          return context
        
        elif user and user.is_active == False:
          signup_data = self._build_resend_dto(signup_form)
          user = UserService.update(user,signup_data, resent_email)
          mail_title, message_data, mail_to = UserService.verify_email_user(request, user.pk, signup_form.email)# 이메일 인증을 위한 데이터 변수들
          send_email.delay(mail_title, message_data, mail_to) # 이메일 인증을 위한 데이터 tasks로 따로 빼둠, 로딩 시간을 줄이기 위해 , 비동기 처리 (celery-redis기능) 
          context = context_infor(
            msg='이메일을 인증해 회원가입을 완료하세요!',
              error=False
              )
          return context
        

    error = signup_form.non_field_errors()
    if error:
      context = context_infor(
        msg=error,
        error=True
      )
      return context
