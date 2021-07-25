from utils import context_infor
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.forms.models import model_to_dict
import json

from news.models import Press, UserPress, Article
from .models import Comment, ReComment, Like
from .dto import CommentCreateDto
from .services import CommentService


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


class CommentCreateView(View):
    
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            print("ajax 요청 받기 성공")
            data = json.loads(request.body)

            comment_dto = self._build_comment_dto(request, data)
            comment = CommentService.create(comment_dto)
            print("댓글 인스턴스 생성")
            context = {
                'comment_pk' : comment.pk,
                'writer' : comment.writer.nickname,
                'writer_img' : comment.writer.image,
                'content' : comment.content,
                'created_time' : comment.created_string
            }
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({"error" : "Error occured during request"}, status=400)

    @staticmethod
    def _build_comment_dto(request, data):
        article_pk = data.get('article_pk')
        article = Article.objects.filter(pk=article_pk).first()
        return CommentCreateDto(
            article=article,
            writer=request.user,
            content=data.get('content'),
            pk=article_pk,
        )

