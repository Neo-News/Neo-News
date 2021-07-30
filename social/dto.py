from dataclasses import dataclass

from user.models import User
from news.models import Article
from .models import Comment

@dataclass
class CommentCreateDto():
   article : Article 
   writer : User
   content : str
   pk : str

@dataclass
class ReCommentCreateDto():
   comment : Comment 
   writer : User
   content : str
   pk : str
