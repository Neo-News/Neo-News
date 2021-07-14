from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email(mail_title, message_data, mail_to):
  """
  유저에게 이메일 인증 링크를 보내는 메서드
  """
  # print('제발 이게 작동해야 한다규.. 제발...')
  email = EmailMessage(mail_title, message_data, to=[mail_to])
  email.send()