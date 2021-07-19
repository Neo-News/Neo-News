import requests
from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/app')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from news.models import Article, Potal,Press,Category
from datetime import datetime
import time

"""
author: son hee jung
date: 0717
description:
daum 뉴스 페이지 카테고리별로 하루치 스크래핑 하는 함수, 카테고리 따로 리스트 받아서 for문을 돌림
코드 리팩토링 필요함(코드 정리, 함수 class로 변경가능?)
"""

insight_news_info = []

# Dict형태로 변환 함수
def dict_infor(**kwargs):
    context = {}
    for k,v in kwargs.items():
        context[k] = v
    return context


category_list = ['society', 'politics']

def parse_daum():
    data = {}
    i = 0
    for cat in category_list:
        category = cat
        for num in range(1,2):
            time.sleep(5)
            print(f'{cat} - {num} 페이지 스크래핑 시작 -!')
            date = datetime.today().strftime("%Y%m%d")
            response = requests.get(f'https://news.daum.net/breakingnews/{cat}?page={num}&regDate={date}')
            soup = BeautifulSoup(response.text, 'html.parser')
    #         category = bg.select_one('#kakaoGnb > div > ul > li.on > a > span.ir_wa')
            ul = soup.select_one('#mArticle > div.box_etc > ul')
            lis = ul.select('ul > li')
            for li in lis:
                try:
                    title = li.select_one('div > strong > a').text
                    ref = li.select_one('div > strong > a')['href']
                    code = ref.split('/')[4]
    #                 print(code)
                    press = li.select_one('strong > span').text
                    press = press.split('·')
                    press = press[0]
                    preview_img = li.select_one('a > img')['src']
                    news_url = requests.get(ref)
                    news_url_html = BeautifulSoup(news_url.text, 'html.parser')
                    category = cat
    #                 print(category)
                    date = news_url_html.select_one('#cSub > div > span > span > span').text
                    date = date.strip()
                    date_list = date.replace(' ','.').split('.')
                    date_list = ' '.join(date_list).split()
                    date_list = date_list[0]+'-'+date_list[1]+'-'+date_list[2]+' '+date_list[3]
                    date_code = datetime.strptime(date_list,'%Y-%m-%d %H:%M')
                    timestamp = time.mktime(date_code.timetuple())
                    timestamp = str(timestamp)
    #                 print(timestamp)
                    content = news_url_html.select_one('#harmonyContainer > section')
                    content = str(content)
                except TypeError:
                    print('error')
                    pass
                # print(insight_news_info)
                insight_news_info = dict_infor( press=press,news_code=code, news_category=category, date=timestamp, preview_img=preview_img, title=title, content=content,ref=ref)
                print(insight_news_info) 
                i += 1
                data[i] = insight_news_info
    return data

if __name__=='__main__':

    news_dict = parse_daum()
    cnt = 0
    # try:
    for v in news_dict.values():
        if not v['preview_img']:
            v['preview_img'] = 'default.img'
        cnt += 1
        if Press.objects.filter(name=v['press']).first() is None:
            Press.objects.create(name = v['press'])
        print('여기까지는 성고오오오오오옹')
        if not Article.objects.filter(title = v['title']):
            Article.objects.create(
                press=Press.objects.filter(name=v['press']).first(),
                potal = Potal.objects.filter(name='다음').first(),
                category=Category.objects.filter(name=v['news_category']).first(),
                code=v['news_code'],
                date=v['date'],
                preview_img=v['preview_img'],
                title=v['title'],
                content=v['content'],
                ref=v['ref'],
                counted_at = 0,
                created_at = time.time()
                    )
              
    # except:
    #     pass