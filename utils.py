import time
import datetime


def context_infor(**kwargs):
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
    
#   print(time_passed)
    if time_passed == 0:
        return '1분 전'
    if time_passed < 60:
        return str(time_passed) + '분 전'
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

