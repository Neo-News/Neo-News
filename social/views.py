from utils import context_infor
from news.models import Press
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import View
import json

class PressEditView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            press_pk = data.get('press_pk')
            Press.objects.filter(pk=press_pk).first().name
            user = request.user
            press = Press.objects.filter(pk=press_pk).first()
            is_deleted = False
            if user not in press.users.all():
                press.users.add(user)
                is_deleted=True
                Press.objects.filter(pk=press_pk).update(
                    deleted_at = True
                )
            
            else:
                press.users.remove(user)
                is_deleted=False
                Press.objects.filter(users__pk = request.user,pk=press_pk).update(
                    deleted_at = False
                )
            context = context_infor(is_deleted=is_deleted)
            
            return JsonResponse(context)
