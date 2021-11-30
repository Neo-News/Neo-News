
from utils import context_info

from user.tasks import send_email
from user.models import User
from user.services import UserService, UserEmailVerifyService


class VerifyEmailMixin():
    def send_verify_email(self, request, dto, form, email):
        try:
            if form.is_valid():
                if email == 'new':
                        user = UserService.create(dto)
                        mail = dto.email

                elif email == 'again':      
                    user = User.objects.get(email=dto.email)
                    resend_email_user = User.objects.get(email=dto.resend_email)
                    
                    if user != resend_email_user:
                        context = context_info(msg='이메일을 확인해주세요 !', error=True)
                        
                        return context

                    user = UserService.update(dto.email, dto.resend_email)
                    mail = dto.resend_email
                
                mail_title, message_data, mail_to = UserEmailVerifyService.verify_email_user(request, user.pk, mail)
            
                send_email.delay(mail_title, message_data, mail_to)
            

                context = context_info(msg='이메일을 인증해 회원가입을 완료하세요!', error=False)
            
                return context

            error = form.non_field_errors()

            if error:
                print(error)

                context = context_info(msg=error, error=True)
                
                return context

        except User.DoesNotExist:
            context = context_info(msg='회원가입부터 해주세요', error=True)
                        
            return context
