from re import S
from news.models import Article, Press, UserPress
from user.models import Category, Keyword
from django.db.models import Q

class ArticleService():
    
    @staticmethod
    def get_articles():
        return Article.objects.all()

    @staticmethod
    def get_article(pk):
        return Article.objects.get(pk = pk)

    @staticmethod
    def get_articles_in_userpress(press_list):
        return [article for article in Article.objects.filter(press__name__in = press_list)]

    @staticmethod
    def get_filter_articles(word):
        return Article.objects.filter(category__name = word)

    @staticmethod
    def get_all_filters_articles(presses, category_name):
        return Article.objects.filter(press__name__in = presses, category__name = category_name)

    @staticmethod
    def get_non_all_filters_articles(keyword):
        return Article.objects.filter(Q(title__contains = keyword) | Q(content__contains = keyword))

    @staticmethod
    def get_include_and_or_filters_articles(keyword, press):
        return Article.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword), press__name__in=press)
    

class CategoryService():

    @staticmethod
    def get_categories():
        return Category.objects.all()

    @staticmethod
    def get_filter_categories(pk):
        return Category.objects.filter(users__pk = pk)

    @staticmethod
    def get_exclude_categories(word):
        return Category.objects.exclude(name=word).all()

    @staticmethod
    def get_category_name(pk):
        return Category.objects.get(pk = pk)

    @staticmethod
    def get_filter_category_users(request, category):
        if request.user in category.users.all():
            category.users.remove(request.user)
        else:
            category.users.add(request.user)

class KeyWordsService():

    @staticmethod
    def get_filter_keywords(pk):
        return Keyword.objects.filter(users__pk = pk)

    @staticmethod
    def get_keyword(pk):
        return Keyword.objects.get(pk = pk)

    @staticmethod
    def get_keyword_name(keyword):
        return Keyword.objects.get(name = keyword)

    @staticmethod
    def create(keyword):
        return Keyword.objects.create(name = keyword)


class UserPressService():
    
    @staticmethod
    def get_userpress(pk):
        return UserPress.objects.get(user__pk = pk)


class PressService():

    @staticmethod
    def get_presses_name(userpress):
        return [press.name for press in userpress.press.all()]
    
    @staticmethod
    def get_presses():
        return Press.objects.all().order_by('name')

    @staticmethod
    def get_non_presses(userpress):
        return userpress.non_press.all()

    @staticmethod
    def get_presses_in_userpress(userpress):
        return userpress.press.all()

