from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField, SetPasswordForm
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _
from user.models import User, UserManager
from django import forms
from django.forms.fields import EmailField
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class UserCreationForm(forms.ModelForm):
    """
    변경 필요 -!!
    """
    # 사용자 생성 폼
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Email address'),
                'required': 'True',
            }
        )
    )
    nickname = forms.CharField(
        label=_('Nickname'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Nickname'),
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label=_('Password')
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(AuthenticationForm):
    """
    author: Oh Ji Yun
    date: 0715
    description: 
    authenticate가 있는 authentication form 상속
    기본적으로 email, password를 렌더링하는데 username=forms.TextInput()이 기본이라 EmailField로 변경
    clean 메서드 안에서 authenticate해주는 로직 있음
    """

    username = EmailField(widget=forms.EmailInput(attrs={'autofocus':True, 'placeholder': _('email'), }))


class SignupForm(forms.Form):
    """
    author: Son Hee Jung
    date: 0713
    description: 
    회원가입 form 커스터마이징, 데이터에 대한 유효성 검증(clean)
    """
    email = forms.CharField(
      label='email',
      required=True,
      widget=forms.EmailInput(
      attrs={
        'class':'user-email',
        'placeholder': 'email',
        'name':'user-email'
      }
    ),
    error_messages={'required': '이메일을 입력해주세요 !'}
    )

    nickname = forms.CharField(
      label='nickname',
      required=True,
      widget=forms.TextInput(
      attrs={
        'class':'user-nickname',
        'placeholder': ' nickname'
      }
    ))

    password = forms.CharField(
      label='password',
      required=False,
      widget=forms.PasswordInput(
      attrs={
        'class':'user-pwd',
        'placeholder': ' password'
      }
    ),)

    password_chk = forms.CharField(
      label='password 확인',
      required=True,
      widget=forms.PasswordInput(
      attrs={
        'class':'user-pwd-chk',
        'placeholder': 're-password'
      }
    ),)
  
    # 폼 input 순서 명시적으로 나열
    # field_order = [
    # 'email',
    # 'nickname',
    # 'password',
    # 'password_chk'
    # ]

  
    # class Meta:
    #     model = get_user_model()
    #     fields = ['email','nickname','password']

    # 회원가입 로직 유효성 검사
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        nickname = cleaned_data.get('nickname')
        password = cleaned_data.get('password')
        password_chk = cleaned_data.get('password_chk')

        if not email or not nickname or not password_chk or not password:
            raise forms.ValidationError('모든 정보를 입력해주세요')

        if '@' not in email or '.' not in email:
            raise forms.ValidationError('올바른 이메일 형식이 아니에요')

        if User.objects.filter(email=email):
            raise forms.ValidationError('이메일이 이미 존재해요')

        if password != password_chk:
            raise forms.ValidationError('비밀번호가 달라요')
        
        elif len(nickname) <= 2:
            raise forms.ValidationError('닉네임을 3자리 이상 지어주세요')

        elif User.objects.filter(nickname=nickname):
            raise forms.ValidationError('닉네임이 이미존재해요')

        self.email = email
        self.nickname = nickname
        self.password = password
        self.password_chk = password_chk


class UserDeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'user-password'}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super.clean()
        password = cleaned_data.get('user_password')
        password_chk = self.user.password

        if password:
            if not check_password(password, password_chk):
                raise forms.ValidationError('비밀번호가 일치하지 않아요')



class VerifyEmailForm(forms.Form):
    pass


class FindPwForm(forms.Form):
    email = forms.CharField(
      label='',
      widget=forms.EmailInput(
      attrs={
        'class':'user-email',
        'placeholder': '이메일 입력',
        'name':'user-email',
      }
    ),
    error_messages={'required': '이메일을 입력해주세요 !'}
    )

    def clean(self):
        cleaned_data = super.clean()
        email = cleaned_data.get('user-email')

        if not email:
           raise forms.ValidationError('이메일을 입력해주세요')


class ChangeSetPwdForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangeSetPwdForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class':'password',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({'class':'password_chk'})
