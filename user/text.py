def message(domain, uidb64, token):
  return f"아래 링크 클릭 프리즈: http://{domain}/user/account/activate/{uidb64}/{token}"