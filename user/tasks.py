import datetime
from celery import shared_task
from django.core.mail import EmailMessage
from news.models import Press, Article, Potal, Category  
from news.daum_scrapping import parse_daum
from django.db.models import Q 
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
    press_list = ['KBS','MBC','경향신문','MBN','SBS','국민일보','노컷뉴스','뉴시스','디스패치','동아일보','매일경제','머니투데이','서울경제','서울신문','세계일보','연합뉴스','이데일리','중앙일보','한국경제','머니S','스포츠조선','스포츠투데이','오마이뉴스','YTN','MK스포츠','베스트일레븐']
    news_dict = parse_daum()
    for v in news_dict.values():
        if Press.objects.filter(name=v['press']):
            print('27개 안에 들어감',v['press'])
            print('여기까지는 성고오오오오오옹')
            
            if not Article.objects.filter(Q(title=v['title']) | Q(content=v['content'])):
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