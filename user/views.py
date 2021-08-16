
import os
import jwt
import json
from kombu.log import Log
import requests
from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.messages.api import success
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic import View, FormView
from django.shortcuts import render, redirect
from boto3.session import Session

from utils import context_infor
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
from news.validate import email_valid_num
from news.models import Press, UserPress
from social.models import Like, Comment
from .dto import SignupDto,ResendDto
from .exception import SocialLoginException, KakaoException
from .forms import FindPwForm, SignupForm, LoginForm, ChangeSetPwdForm,VerificationEmailForm
from .models import User, Category, Keyword
from .mixin import VerifyEmailMixin
from .tasks import send_email
from .services import UserService
from django.contrib.auth.mixins import LoginRequiredMixin



class UserLoginView(FormView):
    """
    author: Oh Ji Yun
    date: 0715
    description:
    FormView 상속받아서 로그인 기능 구현
    Form은 authenticate가 있는 authentication form 사용 
    """
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'
    
    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            auth_login(self.request, user)

        if User.objects.filter(pk=self.request.user.pk).first().is_detailed == False:
            categories = Category.objects.all()
            context = context_infor(categories=categories)
            return render(self.request,'signup_detail.html',context)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.' )
        return super().form_invalid(form)

# 카카오 로그인 뷰
def kakao_login(request):
    """
    author: Oh Ji Yun
    date: 0713
    description: 
    카카오 계정으로 로그인하기 버튼 누르면 authorization server가 정상적인 요청인지 확인
    로그인 페이지로 이동
    로그인 정보 입력하면 authorization server가 authroization_code 응답에 담고, 장고 서버로 redirect
    """
    
    try:
        if request.user.is_authenticated:
            raise SocialLoginException("User arleady logged in")

        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = "http://neonews.site/user/login/social/kakao/callback/"
    
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
        )
    
    except KakaoException as error:
        messages.error(request, error)
        return redirect("index")

    except SocialLoginException as error:
        messages.error(request, error)
        return redirect("index")


# 카카오 로그인 콜백뷰
def kakao_login_callback(request):
    """
    author: Oh Ji Yun
    date: 0713
    description: 
    authorization_code 받고, 콜백 요청이 정상적이라고 판단되면
    code, client_id, client_secret와 함께 access_token 발급 요청 보냄
    authorization server에서 확인하고 인증되면 access_token 발금됨
    발급된 access_token으로 카카로 프로필 api 호출
    이메일, 닉네임 가져와서 유저 생성하고, 로그인 시켜줌    
    """

    try: 
        if request.user.is_authenticated:
            raise SocialLoginException("User arleady logged in")
        code = request.GET.get("code", None)  # code = authorization_code
        if code is None:
            KakaoException("Can't get code")

        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = "http://neonews.site/user/login/social/kakao/callback/"
        client_secret = os.environ.get("KAKAO_SECRET_KEY")
        request_access_token = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}",
            headers={"Accept": "application/json"},
        )
        token_info_json = request_access_token.json()
        error = token_info_json.get("error", None)
        if error is not None:
            KakaoException("Can't get access token")

        access_token = token_info_json.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers=headers,
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")

        nickname = profile.get("nickname", None)
        email = kakao_account.get("email", None)

        user, created = User.objects.get_or_create(email=email)
        if created:
          user.set_password(None)
          user.nickname = nickname
          user.image = "default.png"
          user.is_active = True
          user.is_detailed = True
          user.save()
          auth_login(request, user)
          return redirect("user:signup_detail")
        
        auth_login(request, user)
        return redirect("index")

    except KakaoException as error:
        messages.error(request, error)
        return redirect("index")

    except SocialLoginException as error:
        messages.error(request, error)
        return redirect("index")


class UserSignupView(View):
  """
  author: Son Hee Jung
  date: 0713
  description: 
  회원의 정보를 ajax를 통해 받은 후 데이터를 form(modelformview)으로 보냄,
  formview에서는 데이터 폼에 대한 레이아웃 전송, 정보에 대한 유효성 검증 후 값 리턴
  검증이 끝난 데이터를 user model에 넣어준다. 이때 이메일에 대한 인증을 받기 위해 
  celery의 delay를 통해 비동기적으로 이메일 인증 받는다
  """

  def get(self, request, *args, **kwargs):
    """
    SignupForm을 통해 회원 폼 템플릿에 그려줌
    """
    forms = SignupForm()
    context = {'forms':forms}
    return render(request, 'signup.html',context)
  
  def post(self, request, *args, **kwargs):
    """
    ajax를 통해 회원 정보에 대한 유효성 검증과 유저의 모델을 생성
    """
    if request.is_ajax():
      data = json.loads(request.body)
      print(data)
      signup_form = SignupForm(data)

      if signup_form.is_valid():
        signup_data = self._build_signup_dto(signup_form)
        user = UserService.create(signup_data)
        mail_title, message_data, mail_to = UserService.verify_email_user(request, user.pk, signup_form.email)# 이메일 인증을 위한 데이터 변수들
        send_email.delay(mail_title, message_data, mail_to) # 이메일 인증을 위한 데이터 tasks로 따로 빼둠, 로딩 시간을 줄이기 위해 , 비동기 처리 (celery-redis기능) 
        context = context_infor(error='이메일을 인증해 회원가입을 완료하세요!', is_error=0)
        return JsonResponse(context)

      error = signup_form.non_field_errors()
      if error:
        context = context_infor(error=error, is_error=1)
        return JsonResponse(context) 
  
  @staticmethod
  def _build_signup_dto(data):
    return SignupDto(
      email = data.email,
      nickname = data.nickname,
      password = data.password
    )
        

class Activate(View):
    """
    author: Son Hee Jung
    date: 0713
    description: 
    유저 is_active change, jwt 토큰등 암호화 기능을 이용해서 이메일 인증에 필요한 데이터 생성
    """
    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserService.get_by_user(uid)
        token = jwt.decode(token,'secretkey',algorithm='HS256')
        result = UserService.verify_user_active(user,user.pk, token['user_pk'])
        # auth_login(request, user)
        
        if result:
            return redirect('user:login')
        else:
            return redirect('user:login')


class SignupDeatilView(LoginRequiredMixin,View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self,request, *args, **kwargs):
        categories = Category.objects.exclude(name='속보').all()
        context = context_infor(categories=categories)
        return render(request, 'signup_detail.html', context)

    def post(self, *args, **kwargs):
        pass


# 프로필 이미지 등록하는 함수
class ImageUploadView(View):
    """
    author: Oh Ji Yun
    date: 0711
    description: 
    
    """
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            print("image - ajax 요청 성공")
            data = json.loads(request.body)
            image = data.get('imageURL')
            title = data.get('title')

            # file = request.FILES.get('img')
            session = Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_S3_REGION_NAME
            )
            s3 = session.resource('s3')
            now = datetime.now().strftime('%Y%H%M%S')
            img_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
                Key = now+title,
                Body = image
            )
            s3_url = "https://neonews-s3.s3.ap-northeast-2.amazonaws.com/"
            User.objects.filter(pk=request.user.pk).update(
                # image=now+title
                image=image
            )
            context = { 'msg' : '유저 이미지 수정 성공' }
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({"error" : "Error occured during request"}, status=400)


class UserInforAddView(LoginRequiredMixin,View):
    """
    author: Son Hee Jung
    date: 0715
    description: 
    ajax를 통해 유저가 선택한 카테고리, 키워드 저장 후 메인에 카테고리 띄어줌. 
    is_detailed true로 변환해 설문 페이지 뜨지 않게 설정
    코드 리팩토링 필요함
    """
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            category = Category.objects.all()
            keyword_list = Keyword.objects.all()
            for category in data.get('category_list'):
                category = Category.objects.filter(name=category).first().users.add(request.user)
            for keyword in data.get('todo_list'):
                if not Keyword.objects.filter(name=keyword).first():
                    Keyword.objects.create(
                        name = keyword,
                    )
                Keyword.objects.filter(name=keyword).first().users.add(request.user)
            User.objects.filter(pk=request.user.pk).update(
                is_detailed = True
            )
            presses = Press.objects.all()
            userpress = UserPress.objects.create(
            user = User.objects.filter(pk=request.user.pk).first()
            )
            for press in presses:
                userpress.press.add(press)
            
            return JsonResponse({
                'success':True,
                'url': 'http://neonews.site/'
                })
      

class UserKeywordEditView(LoginRequiredMixin,View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            content = data.get('todo')
            keyword = Keyword.objects.filter(name=content).first()
            if not keyword:
                keyword = Keyword.objects.create(
                    name = content,
                    )
            keyword.users.add(request.user)
            context = context_infor(keyword_pk=keyword.pk, content=content)
            
            return JsonResponse(context)
            

class UserKeywordDeleteView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            keyword_pk = data.get('keyword_pk')
            keyword = Keyword.objects.filter(pk=keyword_pk).first()
            if keyword :
                keyword.users.remove(request.user)
            context = context_infor(is_completed=True)
            
            return JsonResponse(context)


class UserCategoryEditView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            category_pk = data.get('category_pk')
            category = Category.objects.filter(pk=category_pk).first()
            if request.user in category.users.all():
                category.users.remove(request.user)
            else:
                category.users.add(request.user)
            
            categories = Category.objects.filter(users__pk = request.user.pk).all()
            category_list = []
            for category in categories:
                category_list.append(category.name)
            context = context_infor(category_list=category_list)

            return JsonResponse(context)

class ChangePasswordView(LoginRequiredMixin ,View):
    """
    마이페이지의 비밀번호 수정 클래스
    """
    login_url = '/user/login/'
    redirect_field_name='/'
    
    def get(self, request, **kwargs):
        return render(request,'change-password.html')

    def post(self, request, **kwargs):
        session_user = request.session['auth']
        current_user = User.objects.get(email=session_user)
        auth_login(request, current_user)
        return redirect('/')


class DeletePasswordView(LoginRequiredMixin ,View):
    """
    author: Son Hee Jung
    date: 0726
    description: 
    회원 탈퇴 클래스. ajax를 통해 비밀번호를 입력받아 유효성 검증 후 탈퇴가 진행된다
    """
    login_url = '/user/login/'
    redirect_field_name='/'

    def post(self, request, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            password = data.get('password')
            password_chk = request.user.password

        if not password:
            error = True
            msg = '비밀번호를 입력해주세요 !'
            context = context_infor(error=error, msg=msg)
            return JsonResponse(context)

        if not check_password(password, password_chk):
            error = True
            msg = '비밀번호를 틀렸어요 !'
            context = context_infor(error=error, msg=msg)
            return JsonResponse(context)

        User.objects.filter(pk=request.user.pk).update(
            is_active = False
            )
        logout(request)
        messages.success(request, '회원탈퇴 완료 !')
        error = False
        url = 'http://neonews.site/'
        context = context_infor(error=error,url=url)
        return JsonResponse(context)


class FindPwView(View):
    """
    author: Son Hee Jung
    date: 0726
    description: 
    비밀번호 찾기 클래스. 비밀번호 찾기 버튼을 누르면 해당 템플릿으로 이동된다
    """
    template_name = 'find_pw.html'
    find_pw = FindPwForm

    def get(self, request):
        form = self.find_pw(None)
        context = context_infor(form=form)
        return render(request, self.template_name, context)


class PasswordCheckView(View):
    """
    author: Son Hee Jung
    date: 0726
    description: 
    비밀번호 찾기에서 이메일을 입력받아 해당 이메일에 대한 유효성 검증 후 인증번호를
    해당 이메일로 전송한다(celery사용)
    """
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            email=data.get('email')
            user = User.objects.filter(email=email).first()
            
            if not email:
                error = True
                msg = '이메일을 입력해주세요'
                context = context_infor(error=error, msg=msg)    
                return JsonResponse(context)           
            if not user:
                error = True
                msg = '존재하지 않는 이메일이에요'
                context = context_infor(error=error, msg=msg)
                return JsonResponse(context)
            
            auth_num = email_valid_num()
            user.auth = auth_num
            user.save()
            mail_title, message_data, mail_to = UserService.verify_pwd_user(request, user.pk, email, auth_num)# 이메일 인증을 위한 데이터 변수들
            send_email.delay(mail_title, message_data, mail_to) # 이메일 인증을 위한 데이터 tasks로 따로 빼둠, 로딩 시간을 줄이기 위해 , 비동기 처리 (celery-redis기능) 
            context = context_infor(msg='이메일에 인증번호를 발송했습니다!', error=False, auth_num = auth_num)
            return JsonResponse(context)


class PasswordConfirmView(View):
    """
    author: Son Hee Jung
    date: 0726
    description: 
    정상적인 인증번호를 입력했는지에 대한 검증을 하는 클래스. ajax를 이용해 올바르지
    않으면 에러 메시지를 띄어주고 인증된 경우 패스워드 변경 템플릿으로 이동시킨다
    """
    def get(self, request, *args, **kwargs):
        context = context_infor(name = request.user.nickname)
        return render(request,'change-password.html',context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            email=data.get('email')
            auth_num = data.get('valid_num')
            user = User.objects.filter(email=email, auth=auth_num).first()
            if not User.objects.filter(auth=auth_num).first():
                msg = '인증번호가 올바르지 않습니다. 인증번호를 다시한번 확인해주세요 !'
                context = context_infor(success=False,msg=msg) 
                return JsonResponse(context)
            if user:
                user.auth = ''
                user.save()
                request.session['auth'] = user.email
                
                result = json.dumps({'result': user.email})
                context = context_infor(result=result, success=True) 
                return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class ValidChangePassword(View):
    """
    author: Son Hee Jung
    date: 0726
    description: 
    비밀번호를 변경해주는 클래스. SetPasswordForm을 사용하여 비밀번호의 검증을 한 후 실제 유저의 패스워드를 변경한다
    csrf_token관련 문제로 csrf_exempt 데코레이터 사용한 이슈 발생 
    """
    def get(self, request, *args, **kwargs):
        reset_pwd_form = ChangeSetPwdForm(None)
        return render(request, 'valid-change-pwd.html', {'forms':reset_pwd_form})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            session_user = request.session.get('auth')
            current_user = User.objects.get(email = session_user)
            auth_login(request, current_user)
            reset_pwd_form = ChangeSetPwdForm(request.user, data)
            
            if reset_pwd_form.is_valid():
                new_password = reset_pwd_form.cleaned_data['new_password1']
                current_user.set_password(new_password)
                current_user.save()
                logout(request)
                context=context_infor(error=False, url='http://neonews.site/user/login/callback/')
                return JsonResponse(context)
            else:
                logout(request)
                request.session['auth'] = session_user
                error = reset_pwd_form.non_field_errors()
                context = context_infor(msg=error, error=True)
                return JsonResponse(context)


class LoginCallBackView(TemplateView):
    """
    author: Son Hee Jung
    date: 0726
    description: 
    비밀번호 변경후 성공한 템플릿을 화면에 그려준다
    """
    template_name = 'login_callback.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class ResendEmailView(VerifyEmailMixin, View):
    def get(self, request, *args, **kwargs):
        print('get 인증 이메일 View 썽공')
        forms = VerificationEmailForm()
        forms = str(forms)
        context = {'forms':forms}
        return JsonResponse(context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            print('인증 이메일 View 썽공')
            resent_email = data['recent-email']
            change_email = data['email']
            forms = VerificationEmailForm(data)
            context = self.send_verification_email(request, forms ,resent_email = resent_email,change_email=change_email, email='again')
            return JsonResponse(context)

    @staticmethod
    def _build_resend_dto(data):
        return ResendDto(
            email = data.email,
        )


class MypageView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name='/'

    def get(self, request, **kwargs):
        return render(request, 'user-infor.html')

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            print("ajax 요청 받기 성공")
            data = json.loads(request.body)
            nickname = data.get('nickname')
            user = UserService.update_nickname(request, nickname)
            print("유저 닉네임 수정 완료")
            context = {
                'nickname' : user.nickname,
                'msg' : '개인정보가 변경되었습니다.'
            }
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({"error" : "Error occured during request"}, status=400)


class LikeArticleView(LoginRequiredMixin, View):
    login_url = '/user/login/'    
    redirect_field_name='/'

    def get(self, request, **kwargs):
        user = User.objects.filter(pk=request.user.pk).first()
        likes = user.like.all()
        context = context_infor(likes=likes,)
        return render(request, 'user-like.html',context )


class CommentArticleView(LoginRequiredMixin, View):
    login_url = '/user/login/'    
    redirect_field_name='/'

    def get(self, request, **kwargs):
        comments = Comment.objects.filter(writer__pk=request.user.pk)
        context = context_infor(comments=comments)
        return render(request, 'user-comment.html', context)
