import re
import time
import random
import string
import datetime


def context_info(**kwargs):
  a = {}
  for k,v in kwargs.items():
    a[k] = v
  return a


# comment 시간 나타내기
def get_time_passed(created_at):

    now = datetime.datetime.now()
    datetime_format = now.strftime('%Y-%m-%d %H:%M:00')
    current_date = time.mktime(time.strptime(datetime_format,'%Y-%m-%d %H:%M:%S'))
    time_passed = float(current_date)-int(float(created_at))
    
    if time_passed == 0:
        return '1분 전'
    if time_passed < 60:
        return str(int(time_passed)) + '분 전'
    if time_passed//60 < 60:
        return str(int(time_passed//60)) + '분 전'
    if time_passed//(60*60) < 24:
        return str(int(time_passed//(60*60))) + '시간 전'
    if time_passed//(60*60*24) < 30:
        return str(int(time_passed//(60*60*24))) + '일 전'
    if time_passed//(60*60*24*30) < 12:
        return str(int(time_passed//(60*60*24*30))) + '달 전'
    
    else:
        return '오래 전'  


def get_time_passed_comment(created_at):
    current_date = time.time()
    time_passed = float(current_date)-float(created_at)
    
    if time_passed == 0:
        return '1초 전'
    if time_passed < 60:
        return str(int(time_passed)) + '초 전'
    if time_passed//60 < 60:
        return str(int(time_passed//60)) + '분 전'
    if time_passed//(60*60) < 24:
        return str(int(time_passed//(60*60))) + '시간 전'
    if time_passed//(60*60*24) < 30:
        return str(int(time_passed//(60*60*24))) + '일 전'
    if time_passed//(60*60*24*30) < 12:
        return str(int(time_passed//(60*60*24*30))) + '달 전'
    
    else:
        return '오래 전'  


def pwd_regex(string):
    pwd = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
    
    return pwd.match(string)


def email_regex(string):
    email = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    
    return email.match(string)


def email_auth_num():
  LENGTH = 4
  valid_str = string.ascii_letters
  valid_num = ''
  for _ in range(LENGTH):
      valid_num += random.choice(valid_str)
  
  return valid_num
