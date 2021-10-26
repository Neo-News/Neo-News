from dataclasses import dataclass

from user.models import User


@dataclass
class ArticlePkDto():
    pk:int


@dataclass
class CategoryDto():
    category_pk:int
    user_pk:int


@dataclass
class KeywordDto():
    keyword_pk:int
    user_pk:int


@dataclass
class KeywordInforDto():
    keyword:str
    user:User
