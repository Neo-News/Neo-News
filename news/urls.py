from django.urls import path
from news.views import NewsDetailView,NewsInforEditView,CategoryIndexView, KeywordIndexView,NewsInforEditKeywordView, NewsInforEditCategoryView

app_name = 'news'
urlpatterns = [
    path('detail<pk>/', NewsDetailView.as_view() ,name='detail'),
    path('infor/edit/', NewsInforEditView.as_view() ,name='infor-edit'),
    path('infor/edit/keyword/', NewsInforEditKeywordView.as_view() ,name='infor-edit-keyword'),
    path('infor/edit/category/', NewsInforEditCategoryView.as_view() ,name='infor-edit-category'),
    path('category<pk>/', CategoryIndexView.as_view() ,name='category'),
    path('keyword<pk>/', KeywordIndexView.as_view() ,name='keyword'),
]
