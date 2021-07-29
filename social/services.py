from .models import Comment, ReComment
from .dto import CommentCreateDto, ReCommentCreateDto

import time


class CommentService():

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

