from django.db import models
from user.models import User
from news.models import Article
from behaviors import Countable, TimeStampable, Deleteable


class Like(Countable):
    users = models.ManyToManyField(User, blank=True, related_name='like')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='like')


    def __str__(self):
        return self.article.title

    def total_likes(self):
        return self.users.count()


class Comment(TimeStampable,Deleteable):
    article = models.ForeignKey(Article,  on_delete=models.CASCADE, related_name='article') 
    writer = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='my_writer')
    content = models.TextField()

    def __str__(self):
        return self.content


class ReComment(TimeStampable):
    content = models.CharField(max_length=255)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='re_comment')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='re_comment',blank=True)

    def __str__(self):
        return self.content