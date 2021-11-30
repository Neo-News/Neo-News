from celery import shared_task
from django.core.mail import EmailMessage
from news.models import Press, Article, Potal, Category
from social.models import Like  
from news.scrapping import parse_daum, parse_naver, convert_datetime_to_timestamp
from django.db.models import Q 


@shared_task
def send_email(mail_title, message_data, mail_to):
  email = EmailMessage(mail_title, message_data, to=[mail_to])
  email.send()
  return None


@shared_task
def task_scrappy_naver():
    scrappy_list = parse_naver()
    for news in scrappy_list:
        date_list = news['date'].replace(".", " ").replace(":", " ").split(" ")
        time_obj = convert_datetime_to_timestamp(date_list)
        category = Category.objects.filter(name=news['category']).first()
        press = Press.objects.filter(name=news['press']).first()
        if press:
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
                    if not Like.objects.filter(article = article):
                        Like.objects.create(
                            article=article
                        )
    return None


@shared_task
def task_scrappy_daum():
    news_list = parse_daum()
    for news in news_list:
        if Press.objects.filter(name=news['press']).first():
            if not Article.objects.filter(Q(title=news['title']) | Q(content=news['content'])):
                article = Article.objects.create(
                    press=Press.objects.filter(name=news['press']).first(),
                    potal = Potal.objects.filter(name='다음').first(),
                    category=Category.objects.filter(name=news['news_category']).first(),
                    code=news['news_code'],
                    date=news['date'],
                    preview_img=news['preview_img'],
                    kakao_img =news['kakao_img'],
                    title=news['title'],
                    content=news['content'],
                    ref=news['ref'],
                    counted_at = 0,
                    created_at = news['created_at']
                )
                if not Like.objects.filter(article = article):
                    Like.objects.create(
                    article=article
                    )
    return None
