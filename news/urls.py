from django.urls import path
from news.views import NewsDetailView,NewsInforEditView,CategoryIndexView, KeywordIndexView

app_name = 'news'
urlpatterns = [
    path('detail<pk>/', NewsDetailView.as_view() ,name='detail'),
    path('infor/edit/', NewsInforEditView.as_view() ,name='infor-edit'),
    path('category<pk>/', CategoryIndexView.as_view() ,name='category'),
    path('keyword<pk>/', KeywordIndexView.as_view() ,name='keyword'),
]
