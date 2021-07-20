import time

def context_infor(**kwargs):
  a = {}
  for k,v in kwargs.items():
    a[k] = v
  return a



# comment 시간 나타내기
def get_time_passed(object):
    time_passed = int(float(time.time()) - float(object))
    if time_passed == 0:
        return '1초 전'
    if time_passed < 60:
        return str(time_passed) + '초 전'
    if time_passed//60 < 60:
        return str(time_passed//60) + '분 전'
    if time_passed//(60*60) < 24:
        return str(time_passed//(60*60)) + '시간 전'
    if time_passed//(60*60*24) < 30:
        return str(time_passed//(60*60*24)) + '일 전'
    if time_passed//(60*60*24*30) < 12:
        return str(time_passed//(60*60*24*30)) + '달 전'
    else:
        return '오래 전'  
