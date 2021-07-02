from django.shortcuts import render
from django.views.generic import DetailView
# Create your views here.


# 메인페이지 view, 일단은 detailview로 해놓음 , 나중에 카테고리가 생기게 되면 카테고리 pk에 맞는 Article들을 보여줘야 될 것 같아서
class IndexDetailView(DetailView):

  def get(self, request, **kwargs):
    return render(request, 'index.html')


# article list중 하나를 누르면 해당 Article의 Detail 페이지로 이동, 아직 pk받지 않음
class NewsDetailView(DetailView):
  def get(self, request, **kwargs):
    return render(request, 'detail.html')