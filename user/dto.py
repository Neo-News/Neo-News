from dataclasses import dataclass

from user.models import User


@dataclass
class SignupDto():
    email:str
    nickname:str
    password:str


@dataclass
class ResendDto():
    email:str
    recent_email:str


@dataclass
class UserDto():
    password:str
    password_chk:str
    user_pk:int


@dataclass
class UserPkDto():
    pk:int

@dataclass
class VaildEmailDto():
    email:str

  
@dataclass
class UserConfirmDto():
    email:str
    valid_num:int


@dataclass
class AuthDto():
    auth:str
    user:User
