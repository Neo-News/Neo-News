from django.http.response import JsonResponse

from user.services import UserService, UserEmailVerifyService
from user.tasks import send_email
from user.models import User
from user.dto import ResendDto, SignupDto
from utils import context_info


class VerifyEmailMixin:
    def verify_form(self, form):
        if form.is_valid():
            context = context_info(error=False)

            return context
        
        else:
            error = form.non_field_errors()
            context = context_info(msg=error, error=True)

            return context

    def verify_email(self, dto:SignupDto):
        try:
            user = UserService.create(dto)
            mail = dto.email

            return {"user": user, "mail": mail}

        except User.DoesNotExist:
            context = context_info(msg='회원가입부터 해주세요', error=True)

            return JsonResponse(context)
    
    def verify_resend_email(self, dto:ResendDto):
        try:
            user = User.objects.get(email=dto.email)
            resend_email_user = User.objects.get(email=dto.resend_email)

            if user != resend_email_user:
                context = context_info(msg='이메일을 확인해주세요 !', error=True)

                return JsonResponse(context)
            
            user = UserService.update(dto.email, dto.resend_email)
            mail = dto.resend_email

            return {"user": user, "mail": mail, "error":False}

        except User.DoesNotExist:
            context = context_info(msg="회원가입부터 해주세요", error=True)

            return context

    def send_user_email(self, request, mail_info):
        mail_title, message_data, mail_to = UserEmailVerifyService.user_email(request, mail_info["user"].pk, mail_info["mail"])
        
        send_email.delay(mail_title, message_data, mail_to)
    
        context = context_info(msg='이메일을 인증해 회원가입을 완료하세요!', error=False)
        
        return context


