from news.models import Article
from .models import Comment, ReComment, Like
from .dto import CommentCreateDto
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

