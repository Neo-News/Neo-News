from django.urls import path
from news.views import NewsDetailView, NewsInforEditPressView, CategoryView, KeywordIndexView,NewsInforEditKeywordView, NewsInforEditCategoryView

app_name = 'news'
urlpatterns = [
    path('detail/<pk>', NewsDetailView.as_view() ,name='detail'),
    path('infor/edit/press/', NewsInforEditPressView.as_view() ,name='infor-edit'),
    path('infor/edit/keyword/', NewsInforEditKeywordView.as_view() ,name='infor-edit-keyword'),
    path('infor/edit/category/', NewsInforEditCategoryView.as_view() ,name='infor-edit-category'),
    path('category/<pk>', CategoryView.as_view() ,name='category'),
    path('keyword/<pk>', KeywordIndexView.as_view() ,name='keyword'),
]
