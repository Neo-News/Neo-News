from django.http.response import JsonResponse
from utils import context_infor
from user.models import Category, Keyword
from news.models import Article, Press,Potal
from django.shortcuts import redirect, render
from django.views.generic import DetailView,View
from utils import get_time_passed
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import json
#  Create your views here.


# templateview로 변경가능 할 것 같음 일단은 detailview -> view로 변경함 
class IndexView(View):
  """
  참고하셨으면 지우셔도 됩니당 :-)
  다음 스크래핑하면서 데이터를 index에 띄어보느라 코드 작성해 놓았습니다. 
  categories와 keywords는 유저가 선택한 데이터들이 navbar에 보여지기 위해 필터를 사용했습니다
  아직 filter 로직을 따로 빼지는 않았습니다(services.py로 이동시키는것)
  여기서 해결하지 못 한 부분은 기사 미리보기(index화면에 기사 프리뷰부분)에서 컨텐츠를 어떻게 띄어줘야 할지 몰라서 일단은 미리보기 리스트에는 컨텐츠부분을 빼놓았습니다
  (태그를 다같이 스크래핑해와서 이부분이 문제가 생김, 방법이 없는것 같지는 않지만(다시 컨텐츠 부분 스크래핑 , 정규표현식) 의논해봐야 할 것 같아요 ! )
  """
  def get(self, request, **kwargs):
    categories = Category.objects.filter(users__pk=request.user.pk).all()
    keywords = Keyword.objects.filter(users__pk=request.user.pk).all()
    # articles = Article.objects.all()[:20]
    page = request.GET.get('page','1')
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 20)
    try:
        article_obj = paginator.page(page)
    except PageNotAnInteger:
        article_obj = paginator.page(1)
    except EmptyPage:
        article_obj = paginator.page(paginator.num_pages)

#  페이징 번호 5개씩 보이기 로직
    index = article_obj.number
    max_index = len(paginator.page_range)
    page_size = 5
    current_page = int(index) if index else 1
    start_index = int((current_page - 1) / page_size) * page_size
    end_index = start_index + page_size
    if end_index >= max_index:
        end_index = max_index
    page_range = paginator.page_range[start_index:end_index]

    context = context_infor(categories=categories, keywords=keywords, articles=article_obj,page_range=page_range)    
    return render(request, 'index.html',context)

  def post(self, request, **kwargs):
    pass


class NewsDetailView(DetailView):
    """
    참고하셨으면 지우셔도 됩니당 :-)
    기사를 누르면 세부 페이지로 이동시키기 위해 템플릿에서 article의 pk를 함께 보내도록 로직을 변경했습니다. news/detail<pk>/로 url도
    변경했습니다. url로 요청이 오는 로직이 get방식인듯 합니다(이부분 까먹었어요,,ㅋㅋㅋㅋ) 
    해당 기사의 Article 데이터를 filter해온뒤 템플릿에 context로 보냈습니다
    """
    def get(self, request, **kwargs):
        article_list = Article.objects.filter(pk=kwargs['pk']).first()
        context = context_infor(article=article_list)
        return render(request,'detail.html',context)

    # def post(self, request, **kwargs):
    #   return render(request,'detail.html')


# 카테고리나, 키워드 수정하는 페이지
class NewsInforEditView(View):
    def get(self, request, **kwargs):
        
      return render(request, 'infor-edit.html')



class CategoryIndexView(View):
    """
    author: Son Hee Jung
    date: 0720
    description: 
    유저가 누른 카테고리에 대한 기사를 보여주는 클래스입니다
    indexview, keywordindexview와 겹치는 로직이 많으며 
    따로 코드를 분리하는 작업이 필요합니다 
    """
    def get(self, request, **kwargs):
        category_name =Category.objects.filter(pk=kwargs['pk']).first().name
        print(category_name)
        categories = Category.objects.filter(users__pk=request.user.pk).all()
        # articles = Article.objects.filter(category__name=category_name).all()
        keywords = Keyword.objects.filter(users__pk=request.user.pk).all()
        page = request.GET.get('page','1')
        article_list = Article.objects.filter(category__name=category_name).all()
        paginator = Paginator(article_list, 20)
        article_obj = paginator.page(page)
        #  페이징 번호 5개씩 보이기 로직
        index = article_obj.number
        max_index = len(paginator.page_range)
        page_size = 5
        current_page = int(index) if index else 1
        start_index = int((current_page - 1) / page_size) * page_size
        end_index = start_index + page_size
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        
        context = context_infor(articles=article_obj, categories=categories, keywords=keywords, page_range=page_range)
        return render(request,'index.html', context)


class KeywordIndexView(View):
    """
    author: Son Hee Jung
    date: 0720
    description: 
    유저가 누른 키워드에 대한 기사를 보여주는 클래스입니다
    indexview, categoryindexview와 겹치는 로직이 많으며 
    따로 코드를 분리하는 작업이 필요합니다. 키워드는 Q를 import해와 title과 content에 키워드가 존재하는 기사를
    필터해왔습니다
    """
    def get(self, request, **kwargs):
        is_none = False
        msg = ''
        keyword_name =Keyword.objects.filter(pk=kwargs['pk']).first().name
        keywords = Keyword.objects.filter(users__pk=request.user.pk).all()
        articles = Article.objects.filter(Q(title__contains=keyword_name) | Q(content__contains=keyword_name)).all()
        categories = Category.objects.filter(users__pk=request.user.pk).all()
        if not articles:
            is_none = True
            msg = '선택하신 키워드에 관련된 기사가 아직 없어요 -!'
        
        page = request.GET.get('page','1')
        article_list = articles
        paginator = Paginator(article_list, 20)
        article_obj = paginator.page(page)
         #  페이징 번호 5개씩 보이기 로직
        index = article_obj.number
        max_index = len(paginator.page_range)
        page_size = 5
        current_page = int(index) if index else 1
        start_index = int((current_page - 1) / page_size) * page_size
        end_index = start_index + page_size
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context = context_infor(articles=article_obj, categories=categories, keywords=keywords, is_none = is_none, msg=msg, page_range=page_range)
        return render(request,'index.html', context)
