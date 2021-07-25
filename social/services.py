from news.models import Article
from .models import Comment, ReComment, Like
from .dto import CommentCreateDto, ReCommentCreateDto

class CommentService():

    @staticmethod
    def create(dto:CommentCreateDto):
        if dto.content:
            comment = Comment.objects.create(
                article=dto.article,
                writer=dto.writer,
                content=dto.content
            )
        return comment

class ReCommentService():

    @staticmethod
    def create(dto:ReCommentCreateDto):
        if dto.content:
            recomment = ReComment.objects.create(
                comment=dto.comment,
                writer=dto.writer,
                content=dto.content
            )
        return recomment

