import datetime
from celery import shared_task
from django.core.mail import EmailMessage
from news.models import Press, Article, Potal, Category  
from news.daum_scrapping import parse_daum
import time


@shared_task
def send_email(mail_title, message_data, mail_to):
  """
  유저에게 이메일 인증 링크를 보내는 메서드
  """
  # print('제발 이게 작동해야 한다규.. 제발...')
  email = EmailMessage(mail_title, message_data, to=[mail_to])
  print(email)
  email.send()
  print('보내졌는디요...?')
  return None


@shared_task
def task_scrappy():
    news_dict = parse_daum()
    for v in news_dict.values():
        if not v['preview_img']:
            v['preview_img'] = 'default.img'
        if Press.objects.filter(name=v['press']).first() is None:
            Press.objects.create(name = v['press'])
        print('여기까지는 성고오오오오오옹')
        print(datetime.datetime.today())
        if not Article.objects.filter(title = v['title']):
            Article.objects.create(
                press=Press.objects.filter(name=v['press']).first(),
                potal = Potal.objects.filter(name='다음').first(),
                category=Category.objects.filter(name=v['news_category']).first(),
                code=v['news_code'],
                date=v['date'],
                preview_img=v['preview_img'],
                title=v['title'],
                content=v['content'],
                ref=v['ref'],
                counted_at = 0,
                created_at = v['created_at']
                    )            
    return None