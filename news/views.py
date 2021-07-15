from utils import context_infor
from user.models import Category, Keyword
from django.shortcuts import redirect, render
from django.views.generic import DetailView,View
from user.models import User
#  Create your views here.


# 메인페이지 view, 일단은 detailview로 해놓음 , 나중에 카테고리가 생기게 되면 카테고리 pk에 맞는 Article들을 보여줘야 될 것 같아서
class IndexDetailView(DetailView):

  def get(self, request, **kwargs):
    categories = Category.objects.filter(users__pk=request.user.pk).all()
    keywords = Keyword.objects.filter(users__pk=request.user.pk).all()
    context = context_infor(categories=categories, keywords=keywords)    
    print(categories)
    return render(request, 'index.html',context)


# article list중 하나를 누르면 해당 Article의 Detail 페이지로 이동, 아직 pk받지 않음
class NewsDetailView(DetailView):
  def get(self, request, **kwargs):
    return render(request, 'detail.html')


# 카테고리나, 키워드 수정하는 페이지
class NewsInforEditView(View):
    def get(self, request, **kwargs):
      return render(request, 'infor-edit.html')