import string
import random


def email_valid_num():
  LENGTH = 4
  valid_str = string.ascii_letters
  valid_num = ''
  for _ in range(LENGTH):
      valid_num += random.choice(valid_str)

  return valid_num