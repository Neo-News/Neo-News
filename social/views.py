from utils import context_infor
from news.models import Press, UserPress
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.forms.models import model_to_dict
import json

class PressEditView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            press_pk = data.get('press_pk')
            press = Press.objects.filter(pk=press_pk).first()
            # print(press.name)
            user = request.user
            # press = Press.objects.filter(pk=press_pk).first()
            userpress = UserPress.objects.filter(user__pk = user.pk).first()
            print('userpress',userpress)
            # print(userpress)
            is_deleted = False
            if userpress is not None:
                if press not in userpress.press.all():

                    print('해당 언론사 userpress press에 업음')
                    userpress.press.add(press)
                    userpress.non_press.remove(press)
                    is_deleted=True
 
                else:
                    print('60프로성공')
                    userpress.press.remove(press)
                    userpress.non_press.add(press)
                    is_deleted=False

            context = context_infor(is_deleted=is_deleted,press_pk=press_pk,press_obj=model_to_dict(press))
            
            return JsonResponse(context)

