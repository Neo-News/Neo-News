from django.urls import path
from .views import PressEditView, CommentCreateView

app_name = 'social'
urlpatterns = [
    path('press/', PressEditView.as_view() ,name='press'),
    path('comment/', CommentCreateView.as_view() ,name='comment'),
]
