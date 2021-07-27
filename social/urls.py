from django.urls import path
from .views import PressEditView, CommentCreateView, ReCommentCreateView, LikeToggleView

app_name = 'social'
urlpatterns = [
    path('press/', PressEditView.as_view() ,name='press'),
    path('comment/', CommentCreateView.as_view() ,name='comment'),
    path('recomment/', ReCommentCreateView.as_view() ,name='recomment'),
    path('like/', LikeToggleView.as_view() ,name='like'),
]
