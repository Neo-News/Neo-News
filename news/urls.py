from django.urls import path
from news.views import NewsDetailView,NewsInforEditView

app_name = 'news'
urlpatterns = [
    path('detail<pk>/', NewsDetailView.as_view() ,name='detail'),
    path('infor/edit/', NewsInforEditView.as_view() ,name='infor-edit'),
]
