from django.shortcuts import render
from django.views.generic import DetailView
# Create your views here.


class IndexDetailView(DetailView):

  def get(self, request, **kwargs):
    return render(request, 'index.html')