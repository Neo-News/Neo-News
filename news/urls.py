from django.urls import path
from news.views import NewsDetailView

app_name = 'news'
urlpatterns = [
    path('detail/', NewsDetailView.as_view() ,name='detail'),
]
