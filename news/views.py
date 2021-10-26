from django.shortcuts import render
from django.views.generic import DetailView,View
from django.views.generic import ListView
from utils import context_infor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, View
from social.services import CommentService, LikeService
from news.services import CategoryService, KeyWordsService, ArticleService, PressService, UserPressService
from news.dto import ArticlePkDto, CategoryDto, KeywordDto
from .utils import paging


class IndexView(View):

    def get(self, request, **kwargs):
        data = self._build_article_pk(request)
        categories = CategoryService.get_filter_categories(data.pk)
        keywords = KeyWordsService.get_filter_keywords(data.pk)
        article_list = ArticleService.get_articles()
        if request.user.is_authenticated :
            userpress = UserPressService.get_userpress(data.pk)
            if userpress is not None:
                press_list = PressService.get_presses_name(userpress)
                article_list = ArticleService.get_articles_in_userpress(press_list)

        page_range, article_obj = paging(request.GET.get('page','1'), article_list, 20)
        context = context_infor(
                                categories=categories,
                                keywords=keywords, 
                                articles=article_obj,
                                page_range=page_range
                                )    
        return render(request, 'index.html', context)
    
    def _build_article_pk(self, request):
        return ArticlePkDto(
            pk = request.user.pk
        )


class NewsDetailView(LoginRequiredMixin, DetailView):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self, request, **kwargs):
        data = self._build_article_pk()
        article = ArticleService.get_article(data.pk)
        comments = CommentService.get_filter_comment(data.pk)
        like = LikeService.get_like(data.pk)
        is_liked = LikeService.get_like_state(like, request.user)
        context = context_infor(
                                article=article, 
                                comments=comments, 
                                like=like, 
                                is_liked=is_liked
                                )
        return render(request,'detail.html',context)

    def _build_article_pk(self):
        return ArticlePkDto(
            pk = self.kwargs['pk']
        )
    

class NewsInforEditPressView(LoginRequiredMixin, ListView):
    login_url = 'user/login/'
    redirect_field_name='/'
    
    def get(self, request, **kwargs):
        data = self._build_article_pk(request)
        userpress = UserPressService.get_userpress(data.pk)
        presses = PressService.get_presses()
        non_press = PressService.get_non_presses(userpress)
        press = PressService.get_presses_in_userpress(userpress)
        page_range, press_obj = paging(request.GET.get('page','1'), presses, 10)
        context = context_infor(presses=press_obj, 
                                page_range=page_range,
                                in_press=press,
                                non_press=non_press,
                                )    
        return render(request, 'infor-edit.html',context)

    def _build_article_pk(self, request):
        return ArticlePkDto(
            pk = request.user.pk
        )
    

class NewsInforEditKeywordView(View):
    def get(self, request, **kwargs):
        data = self._build_article_pk(request)
        keywords = KeyWordsService.get_filter_keywords(data.pk)
        context = context_infor(keywords=keywords)
        return render(request, 'infor-keyword.html', context)

    def _build_article_pk(self, request):
        return ArticlePkDto(
            pk = request.user.pk
        )


class NewsInforEditCategoryView(View):
    def get(self, request, **kwargs):
        data = self._build_article_pk(request)
        categories = CategoryService.get_exclude_categories('속보')
        user_categories = CategoryService.get_filter_categories(data.pk)
        context = context_infor(categories=categories, user_categories=user_categories)
        return render(request, 'infor-category.html', context)

    def _build_article_pk(self, request):
        return ArticlePkDto(
            pk = request.user.pk
        )


class CategoryView(View):

    def get(self, request, **kwargs):
        data = self._build_category_dto(request)
        category_name = CategoryService.get_category_name(data.category_pk).name
        categories = CategoryService.get_filter_categories(data.user_pk)
        keywords = KeyWordsService.get_filter_keywords(data.user_pk)
        article_list = ArticleService.get_filter_articles(category_name)
        if request.user.is_authenticated :
            userpress = UserPressService.get_userpress(data.user_pk)
            if userpress is not None:
                press_list = PressService.get_presses_name(userpress)
                article_list = ArticleService.get_all_filters_articles(press_list, category_name)
            page_range, article_obj = paging(request.GET.get('page','1'), article_list, 20)
            context = context_infor(
                                    categories=categories,
                                    keywords=keywords, 
                                    articles=article_obj,
                                    page_range=page_range
                                    )    
        return render(request,'index.html', context)

    def _build_category_dto(self, request):
        return CategoryDto(
            user_pk = request.user.pk,
            category_pk = self.kwargs['pk']
        )


class KeywordIndexView(View):

    def get(self, request, **kwargs):
        is_none = False
        msg = ''
        data = self._build_keyword_dto(request)
        keyword_name = KeyWordsService.get_keyword(data.keyword_pk).name
        keywords = KeyWordsService.get_filter_keywords(data.user_pk)
        article_list = ArticleService.get_non_all_filters_articles(keyword_name)
        categories = CategoryService.get_filter_categories(data.user_pk)

        if not article_list:
            is_none = True
            msg = '선택하신 키워드에 관련된 기사가 아직 없어요 -!'
        if request.user.is_authenticated :
            userpress = UserPressService.get_userpress(data.user_pk)
            if userpress is not None:
                press_list = PressService.get_presses_name(userpress)
                article_list = ArticleService.get_include_and_or_filters_articles(keyword_name, press_list)

        page_range, article_obj = paging(request.GET.get('page','1'), article_list, 20)                 
        context = context_infor(
                                articles=article_obj, 
                                categories=categories, 
                                keywords=keywords, 
                                is_none=is_none, 
                                msg=msg, 
                                page_range=page_range
                                )
        return render(request,'index.html', context)

    def _build_keyword_dto(self, request):
        return KeywordDto(
            keyword_pk = self.kwargs['pk'],
            user_pk = request.user.pk
        )
