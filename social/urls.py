from django.urls import path
from .views import PressEditView


app_name = 'social'
urlpatterns = [
    path('press/', PressEditView.as_view() ,name='press'),
]
