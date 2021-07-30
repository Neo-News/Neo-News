from django.db import models
from user.models import User
from behaviors import TimeStampable, Countable, Deleteable
from user.models import User,Category, Keyword
import time
import datetime
from utils import get_time_passed


class Press(Deleteable):
    name = models.CharField(max_length=32)
    is_checked = models.BooleanField(default=True)
    def __str__(self):
      return self.name


class UserPress(Deleteable):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user')
    press = models.ManyToManyField(Press,blank=True, related_name='user_press')
    non_press = models.ManyToManyField(Press, blank=True, related_name='non_press')
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
    kakao_img = models.URLField()
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
      created_time = get_time_passed(self.created_at)
      return created_time

  
class ArticleShare(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='article_share')
    users = models.ManyToManyField(User, blank=True, related_name='article_share')
  

    def total_likes(self):
      return self.users.count()