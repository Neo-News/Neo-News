from django.db import models
from user.models import User
from behaviors import TimeStampable, Countable, Deleteable
from user.models import User,Category, Keyword
import time
import datetime


class Press(Deleteable):
    name = models.CharField(max_length=32)
    def __str__(self):
      return self.name


class UserPress(Deleteable):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user')
    press = models.ManyToManyField(Press,blank=True, related_name='user_press')
    is_checked = models.BooleanField(default=True)


class Potal(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
      return self.name


class Article(TimeStampable, Countable):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='article')
    press = models.ForeignKey(Press, on_delete=models.SET_NULL, null=True, related_name='press')
    potal = models.ForeignKey(Potal, on_delete=models.SET_NULL, null=True, related_name='potal')
    code = models.CharField(max_length=62)
    preview_img = models.TextField(default='default.png',blank=True)
    title = models.CharField(max_length=124)
    content = models.TextField()
    date = models.TextField()
    ref = models.URLField()

    class Meta:
      ordering = ['-created_at','-date']

    def __str__(self):
      return f'{self.category}- {self.potal.name}-{self.title}'

    @property
    def created_string(self):
      """
      참고하셨으면 지우셔도 됩니당 :-)
      스크래핑한 기사 시간을 현재 시간에서 빼주어 총 몇 초 차이가 나는지 계산하였고 나온 값을 아래와 같은
      로직을 사용하여 ~초전 ~분전으로 나올 수 있게 하였습니다. 이때 다음기사는 년,월,일,시,분만 제공을 해주기 때문에
      초를 없앤 후 계산하였습니다.datetime_format과 current_date부분이 현재 시간을 Time으로 받은뒤
      초를 생략하여 계산한 로직입니다 (원래 time은 초까지 계산함) 
      """
      now = datetime.datetime.now()
      datetime_format = now.strftime('%Y-%m-%d %H:%M:00')
      current_date = time.mktime(time.strptime(datetime_format,'%Y-%m-%d %H:%M:%S'))

      time_passed = float(current_date)-int(float(self.created_at))
    #   print(time_passed)
      if time_passed == 0:
          return '1분 전'
      if time_passed < 60:
          return str(time_passed) + '분 전'
      if time_passed//60 < 60:
          return str(int(time_passed//60)) + '분 전'
      if time_passed//(60*60) < 24:
          return str(int(time_passed//(60*60))) + '시간 전'
      if time_passed//(60*60*24) < 30:
          return str(int(time_passed//(60*60*24))) + '일 전'
      if time_passed//(60*60*24*30) < 12:
          return str(int(time_passed//(60*60*24*30))) + '달 전'
      else:
          return '오래 전'  

  
class ArticleShare(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='article_share')
    users = models.ManyToManyField(User, blank=True, related_name='article_share')

    def total_likes(self):
      return self.users.count()