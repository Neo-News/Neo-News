import time
from .models import Comment, ReComment
from .dto import CommentCreateDto, ReCommentCreateDto
from social.models import Comment, Like


class CommentService():

    @staticmethod
    def get_filter_comment(pk):
        return Comment.objects.filter(article__pk = pk)

    @staticmethod
    def get_user_comment(pk):
        return  Comment.objects.filter(writer__pk = pk)

    @staticmethod
    def create(dto:CommentCreateDto):
        if dto.content:
            comment = Comment.objects.create(
                article=dto.article,
                writer=dto.writer,
                content=dto.content,
                created_at = time.time()
            )
        return comment


class ReCommentService():

    @staticmethod
    def create(dto:ReCommentCreateDto):
        if dto.content:
            recomment = ReComment.objects.create(
                comment=dto.comment,
                writer=dto.writer,
                content=dto.content,
                created_at=time.time()
            )
        return recomment


class LikeService():

    @staticmethod
    def get_like(pk):
        return Like.objects.get(article__pk = pk)

    @staticmethod
    def get_like_state(like, user):
        return True if user in like.users.all() else False
