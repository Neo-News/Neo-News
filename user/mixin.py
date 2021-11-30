from utils import context_infor
from user.dto import ResendDto
from user.tasks import send_email
from user.models import User
from user.services import UserService, UserEmailVerifyService


class VerifyEmailMixin():
    def send_verify_email(self, request, dto:ResendDto, signup_form, email):
        try:
            if signup_form.is_valid():
                if email == 'new':
                        pass
                #   signup_data = self._build_signup_dto(signup_form)
                #   user = UserService.create(signup_data)
                #   mail_title, message_data, mail_to = UserService.verify_email_user(request, user.pk, signup_form.email)# 이메일 인증을 위한 데이터 변수들
                #   send_email.delay(mail_title, message_data, mail_to) # 이메일 인증을 위한 데이터 tasks로 따로 빼둠, 로딩 시간을 줄이기 위해 , 비동기 처리 (celery-redis기능) 
                #   context = context_infor(
                #   msg='이메일을 인증해 회원가입을 완료하세요!',
                #     error=False
                #     )
                #   return context

                elif email == 'again':      
                    user = User.objects.get(email=dto.email)
                    resend_email_user = User.objects.get(email=dto.resend_email)
                    
                    if user != resend_email_user:
                        context = context_infor(msg='이메일을 확인해주세요 !', error=True)
                        
                        return context

                    if user.is_active == False:
                        user = UserService.update(dto.email, dto.resend_email)
                        mail_title, message_data, mail_to = UserEmailVerifyService.verify_email_user(request, user.pk, dto.resend_email)
                        
                        send_email.delay(mail_title, message_data, mail_to)
                        
                        context = context_infor(msg='이메일을 인증해 회원가입을 완료하세요!', error=False)
                        
                        return context

            error = signup_form.non_field_errors()

            if error:
                context = context_infor(msg=error, error=True)
                return context
        
        except User.DoesNotExist:
            context = context_infor(msg='회원가입부터 해주세요', error=True)
                        
            return context
            
