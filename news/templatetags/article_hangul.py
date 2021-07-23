from django import template
import re

register = template.Library()

@register.filter
def get_hangul(value):
    value = value
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('',value).strip()
    return result

@register.filter
def get_hangul_num(value):
    value = value
    hangul = re.compile('[^ ㄱ-ㅣ가-힣0-9]+')
    result = hangul.sub('',value).strip()
    return result 