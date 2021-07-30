import datetime
from celery import shared_task
from django.core.mail import EmailMessage
from news.models import Press, Article, Potal, Category
from social.models import Like  
from news.scrapping import parse_daum, parse_naver, convert_datetime_to_timestamp
from django_celery_beat.models import PeriodicTask, IntervalSchedule
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
def task_scrappy_naver():
    # 네이버 스크래핑
    scrappy_list = parse_naver()
    print("스크래핑 성공")

    for news in scrappy_list:
        date_list = news['date'].replace(".", " ").replace(":", " ").split(" ")
        time_obj = convert_datetime_to_timestamp(date_list)
        category = Category.objects.filter(name=news['category']).first()
        press = Press.objects.filter(name=news['press']).first()
        if not press:
            press = Press.objects.create(name=news['press'])
        
        if news['category'] == "생활/문화":
            category = Category.objects.filter(name='문화').first()
        
        if news['category'] == "IT/과학":
            category = Category.objects.filter(name='IT').first()
        
        if news['category'] == "세계":
            category = Category.objects.filter(name='국제').first()
        
        if Press.objects.filter(name=news['press']):
            if not Article.objects.filter(Q(title=news['title']) | Q(content=news['content'])):
                article = Article.objects.create(
                    category=category,
                    press=press,
                    potal=Potal.objects.filter(name="네이버").first(),
                    code=news['code'],
                    preview_img=news['preview_img'],
                    kakao_img =news['kakao_img'],
                    title=news['title'],
                    content=news['content'],
                    date=news['date'],
                    ref=news['ref'],
                    counted_at = 0,
                    created_at=time_obj,
                    )
                print("기사 DB 넣기 성공")
                if not Like.objects.filter(article = article):
                    Like.objects.create(
                        article=article
                    )
                    print("좋아요 인스턴스 생성")
    return None


@shared_task
def task_scrappy_daum():
    news_dict = parse_daum()
    for v in news_dict.values():
        if Press.objects.filter(name=v['press']):
            print('여기까지는 성고오오오오오옹')
            if not Article.objects.filter(Q(title=v['title']) | Q(content=v['content'])):
                article = Article.objects.create(
                    press=Press.objects.filter(name=v['press']).first(),
                    potal = Potal.objects.filter(name='다음').first(),
                    category=Category.objects.filter(name=v['news_category']).first(),
                    code=v['news_code'],
                    date=v['date'],
                    preview_img=v['preview_img'],
                    kakao_img =v['kakao_img'],
                    title=v['title'],
                    content=v['content'],
                    ref=v['ref'],
                    counted_at = 0,
                    created_at = v['created_at']
                )
                if not Like.objects.filter(article = article):
                    Like.objects.create(
                    article=article
                    )
    return None