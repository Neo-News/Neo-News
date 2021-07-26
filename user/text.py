def message(domain, uidb64, token):
  return f"인증에 성공 하셨습니다. :-) 아래 링크 클릭해서 회원가입을 해주세요 ! \n http://{domain}/user/account/activate/{uidb64}/{token}"

def pwd_change_message(auth_num):
  return f"인증번호 : {auth_num} 를 입력해주세요."