from django.db import models
from user.models import User
from news.models import Article
from behaviors import Countable, TimeStampable, Deleteable
from utils import get_time_passed, get_time_passed_comment


class Like(Countable):
    users = models.ManyToManyField(User, blank=True, related_name='like')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='like')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return self.article.title

    @property
    def total_likes(self):
        return self.users.count()


class Comment(TimeStampable,Deleteable):
    article = models.ForeignKey(Article,  on_delete=models.CASCADE, related_name='comment') 
    writer = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()

    def __str__(self):
        return self.content

    @property
    def created_string(self):
      created_time = get_time_passed_comment(self.created_at)
      return created_time


class ReComment(TimeStampable, Deleteable):
    content = models.CharField(max_length=255)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='re_comment')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='re_comment',blank=True)

    def __str__(self):
        return self.content

    @property
    def created_string(self):
      created_time = get_time_passed_comment(self.created_at)
      return created_time

    