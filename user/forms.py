from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from user.models import User, UserManager
from django import forms
from django.forms.fields import EmailField
from django.contrib.auth.hashers import check_password
from utils import pwd_regex, email_regex


class UserCreationForm(forms.ModelForm):

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
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('Password')
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus':True, 'placeholder': _('email'), }))


class SignupForm(forms.Form):

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
  
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        nickname = cleaned_data.get('nickname')
        password = cleaned_data.get('password')
        password_chk = cleaned_data.get('password_chk')
        email_type = email_regex(email)
        pwd_type = pwd_regex(password)
        if not email or not nickname or not password_chk or not password:
            raise forms.ValidationError('모든 정보를 입력해주세요')

        elif not email_type:
            raise forms.ValidationError('올바른 이메일 형식이 아니에요')

        elif User.objects.filter(email=email):
            raise forms.ValidationError('이메일이 이미 존재해요. 해당 이메일 재인증을 받으시려면 아래 버튼을 눌러주세요')

        elif password != password_chk:
            raise forms.ValidationError('비밀번호가 달라요')
        
        elif not pwd_type:
            raise forms.ValidationError('비밀번호는 최소 8자리 이상, 1개 이상의 숫자와 문자,특수문자가 들어가야 합니다')

        elif len(nickname) <= 1:
            raise forms.ValidationError('닉네임을 2자리 이상 지어주세요')

        elif User.objects.filter(nickname=nickname):
            raise forms.ValidationError('닉네임이 이미 존재해요')


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
        self.fields['new_password1'].widget.attrs.update({'class':'password','placeholder': '비밀번호 입력'})
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({'class':'password_chk','placeholder': '비밀번호 확인'})

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('new_password1')
        password_2 = cleaned_data.get('new_password2')
        try:
            pwd_type = pwd_regex(password_1)
        except:
            pwd_type = None
            pass

        if not pwd_type:
            raise forms.ValidationError('비밀번호의 조건을 다시한번 확인해주세요')
        if not password_1 or not password_2:
            raise forms.ValidationError('값을 전부 입력해주세요')



class VerificationEmailForm(forms.Form):
    email = forms.CharField(
    label='',
    required=True,
    widget=forms.EmailInput(
    attrs={
        'class':'resend-input',
        'placeholder': '이메일을 입력하세요'
    }
    ),)
  
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not email:
            raise forms.ValidationError('재인증 받고 싶은 이메일을 위쪽에 먼저 입력해주세요 !')

        elif not User.objects.filter(email=email).exists():
            raise forms.ValidationError('회원가입 되지 않은 이메일입니다. 회원가입부터 해주세요 !')

        elif User.objects.filter(email=email, is_active=True).first():
            raise forms.ValidationError('이미 가입되어 있는 이메일입니다. 다른 이메일을 입력해주세요 !')

        self.email = email
