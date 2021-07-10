from django.contrib import admin
from user.models import User,LoginLog, Category, Keyword
from social.models import Like, Comment, ReComment
from news.models import Article, Potal, Press, ArticleShare


admin.site.register(User)
admin.site.register(LoginLog) 
admin.site.register(Category)
admin.site.register(Keyword)
admin.site.register(Article)
admin.site.register(Potal)
admin.site.register(Press)
admin.site.register(ArticleShare)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(ReComment)
