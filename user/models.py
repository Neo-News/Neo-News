from behaviors import Deleteable, TimeStampable
from django.db import models
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (
  BaseUserManager, AbstractBaseUser, PermissionsMixin
    )


class UserManager(BaseUserManager):
    """
    사용자 정보 관리 클래스로 사용자를 등록하는 역학을 한다. 이 과정에서 일반 사용자인 경우엔 어떻게
    상태를 어떻게 정의하고 등록할 것인지, 관리자인 경우에 어떻게 등록할지 그 동작하는 것들을 미리 정의해두고 수행할 수 있도록
    만든 클래스이다.
    """

    def create_user(self, email, nickname, image, password=None):
        """
        주어진 이메일, 닉네임, url, 비밀번호 등 개인정보로 User 인스턴스 생성
        url은 profile image url인데 네이밍 생각중/ 기본적으로는 wikidocs에 나와있는 상속 커스터마이징과 비슷함
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            url = image
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password, image='none'):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        url쓰고 싶지 않았는데 쓰지 않으면 createsuperuser할때 url 없다고 error 발생.. 이유를 잘 모르겠음, 암튼 위에서 none이라는 문자열 넣어줌
        """
        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
            image = image
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampable, Deleteable):
    """
    장고의 auth앱에 있는 모델 클래스로 사용자 정보의 기본적인 형태를 갖는 추상적인  형태의 
    클래스, 사용자가 가져야 할 최소한의 정보를 갖는 클래스를 상속받아 user 클래스를 생성함
    """
    image = models.TextField(
        verbose_name=('Profile image'),
    )
    email = models.EmailField(
        verbose_name=('Email address'),
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name=('Nickname'),
        max_length=30,
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name=('Is active'),
        default=False
    )

    objects = UserManager() 


    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['nickname', ]


    def __str__(self):
        return self.nickname

    def get_full_name(self):        
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def get_id(self):
        return self.id

    @property
    def is_staff(self):
        
        return self.is_superuser

    get_full_name.short_description = ('Full name')


class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='login_log')
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user} , {self.ip_address}'


class Category(models.Model):
    users = models.ManyToManyField(User, blank=True, related_name='category')
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    users = models.ManyToManyField(User, blank=True, related_name='keyword')
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

          