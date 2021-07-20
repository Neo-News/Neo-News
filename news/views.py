from django.http.response import JsonResponse
from utils import context_infor
from user.models import Category, Keyword
from news.models import Article, Press,Potal
from django.shortcuts import redirect, render
from django.views.generic import DetailView,View
from user.models import User
from utils import get_time_passed
from django.core.serializers import serialize
from django.db.models import Q

import re
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
    articles = Article.objects.all()[:20]
    context = context_infor(categories=categories, keywords=keywords, articles=articles)    
    return render(request, 'index.html',context)

  def post(self, request, **kwargs):
    if request.is_ajax():
      data = json.loads(request.body)
      articles = Article.objects.filter(category__pk=data['category_pk']).all()[:20]
      article_list = [{
        'pk' : article.id,
        'title' : article.title,
        'content' : article.content,
        'potal' : Potal.objects.filter(name=article.potal).first().name,
        'press' : Press.objects.filter(name=article.press).first().name,
        'preview_img' : article.preview_img,
        'date' : get_time_passed(article.date),
      } for article in Article.objects.filter(category__pk=data['category_pk']).all()[:15]]
      
      return JsonResponse({'article_list': article_list})


class NewsDetailView(DetailView):
  """
  참고하셨으면 지우셔도 됩니당 :-)
  기사를 누르면 세부 페이지로 이동시키기 위해 템플릿에서 article의 pk를 함께 보내도록 로직을 변경했습니다. news/detail<pk>/로 url도
  변경했습니다. url로 요청이 오는 로직이 get방식인듯 합니다(이부분 까먹었어요,,ㅋㅋㅋㅋ) 
  해당 기사의 Article 데이터를 filter해온뒤 템플릿에 context로 보냈습니다
  """
  def get(self, request, **kwargs):
    article = Article.objects.filter(pk=kwargs['pk']).first()
    context = context_infor(article=article)
    return render(request,'detail.html',context)
  
  # def post(self, request, **kwargs):
  #   return render(request,'detail.html')


# 카테고리나, 키워드 수정하는 페이지
class NewsInforEditView(View):
    def get(self, request, **kwargs):
      return render(request, 'infor-edit.html')



class CategoryIndexView(View):
  def get(self, request, **kwargs):
    category_name =Category.objects.filter(pk=kwargs['pk']).first().name
    print(category_name)
    categories = Category.objects.filter(users__pk=request.user.pk).all()
    articles = Article.objects.filter(category__name=category_name).all()[:20]
    keywords = Keyword.objects.filter(users__pk=request.user.pk).all()
    context = context_infor(articles=articles, categories=categories, keywords=keywords)
    return render(request,'index.html', context)


class KeywordIndexView(View):
  def get(self, request, **kwargs):
    is_none = False
    msg = ''
    keyword_name =Keyword.objects.filter(pk=kwargs['pk']).first().name
    keywords = Keyword.objects.filter(users__pk=request.user.pk).all()
    articles = Article.objects.filter(Q(title__contains=keyword_name) | Q(content__contains=keyword_name)).all()[:20]
    categories = Category.objects.filter(users__pk=request.user.pk).all()
    if not articles:
      is_none = True
      msg = '선택하신 키워드에 관련된 기사가 아직 없어요 -!'
    context = context_infor(articles=articles, categories=categories, keywords=keywords, is_none = is_none, msg=msg)
    return render(request,'index.html', context)
