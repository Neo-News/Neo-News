def message(domain, uidb64, token):
  return f"아래 링크 클릭 프리즈: http://{domain}/user/account/activate/{uidb64}/{token}"

def pwd_change_message(domain, uidb64, token, auth_num):
  return f"아래 링크를 클릭해서 인증번호 : {auth_num}를 입력해주세요. : http://{domain}/user/password/activate/{uidb64}/{token}'"