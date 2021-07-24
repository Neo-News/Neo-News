from dataclasses import dataclass

from user.models import User
from .models import Article

@dataclass
class CommentCreateDto():
   article : Article 
   writer : User
   content : str
   pk : str
