import json
from django.forms.models import model_to_dict
from utils import context_info
from django.http.response import JsonResponse
from django.views.generic import View
from news.models import Press, UserPress, Article
from .dto import CommentCreateDto, ReCommentCreateDto
from .models import Comment, ReComment, Like
from .services import CommentService, ReCommentService


class PressEditView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            press_pk = data.get('press_pk')
            press = Press.objects.filter(pk=press_pk).first()
            user = request.user
            userpress = UserPress.objects.filter(user__pk = user.pk).first()
            is_deleted = False
            if userpress is not None:
                if press not in userpress.press.all():
                    userpress.press.add(press)
                    userpress.non_press.remove(press)
                    is_deleted=True
                else:
                    userpress.press.remove(press)
                    userpress.non_press.add(press)
                    is_deleted=False

            context = context_info(is_deleted=is_deleted,press_pk=press_pk,press_obj=model_to_dict(press))
            return JsonResponse(context)


class CommentCreateView(View):
    
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            data = json.loads(request.body)

            comment_dto = self._build_comment_dto(request, data)
            comment = CommentService.create(comment_dto)
            recomments = ReComment.objects.filter(comment__pk=comment.pk)
            total_recomments = [recomment for recomment in recomments]

            context = {
                'comment_pk' : comment.pk,
                'writer' : comment.writer.nickname,
                'writer_img' : comment.writer.image,
                'content' : comment.content,
                'created_time' : comment.created_string,
                'total_recomments' : len(total_recomments)
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

        
class ReCommentCreateView(View):

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            data = json.loads(request.body)
            recomment_dto = self._build_recomment_dto(request, data)
            recomment = ReCommentService.create(recomment_dto)
            context = {
                'recomment_pk' : recomment.pk,
                'writer' : recomment.writer.nickname,
                'writer_img' : recomment.writer.image,
                'content' : recomment.content,
                'created_time' : recomment.created_string,
            }
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({"error" : "Error occured during request"}, status=400)

    @staticmethod
    def _build_recomment_dto(request, data):
        comment_pk = data.get('comment_pk')
        comment = Comment.objects.filter(pk=comment_pk).first()
        return ReCommentCreateDto(
            comment=comment,
            writer=request.user,
            content=data.get('content'),
            pk=comment_pk,
        )

class LikeToggleView(View):

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            context = {}
            data = json.loads(request.body)
            article_pk = data.get('article_pk')
            like = Like.objects.filter(article__pk=article_pk).first()
            if request.user in like.users.all():
                like.users.remove(request.user)
                context = {
                    'is_liked' : False,
                    'count' : like.total_likes,
                }
                return JsonResponse(context, status=200)

            like.users.add(request.user)
            context = {
                'is_liked' : True,
                'count' : like.total_likes,
            }
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({"error" : "Error occured during request"}, status=400)