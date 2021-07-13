from django.db import models
from user.models import User
from behaviors import TimeStampable, Countable
from user.models import Category, Keyword


class Press(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
      return self.name


class Potal(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
      return self.name


class Article(TimeStampable, Countable):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='article')
    press = models.ForeignKey(Press, on_delete=models.SET_NULL, null=True, related_name='press')
    potal = models.ForeignKey(Potal, on_delete=models.SET_NULL, null=True, related_name='potal')
    code = models.CharField(max_length=62)
    preview_img = models.TextField()
    title = models.CharField(max_length=124)
    content = models.TextField()
    date = models.TextField()
    ref = models.URLField()

    class Meta:
      ordering = ['created_at', '-date']

    def __str__(self):
      return f'{self.code}- {self.date}'

  
class ArticleShare(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='article_share')
    users = models.ManyToManyField(User, blank=True, related_name='article_share')

    def total_likes(self):
      return self.users.count()