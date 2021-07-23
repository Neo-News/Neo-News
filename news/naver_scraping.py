
import requests
from bs4 import BeautifulSoup
from requests.api import head
import time, datetime

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/app')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()


from user.models import Category
from news.models import Potal, Press, Article

"""
author: Oh Ji Yun
date: 0720
description: 
네이버 뉴스 카테고리별로 하루치 스크래핑 하는 함수
스크래핑한 데이터 DB에 넣어주기
for문 때문에 depth가 깊어서 리팩토링 필요
"""

# datetime -> time 객체로 만들어줌
def convert_datetime_to_timestamp(date_list):
    if date_list[4] == "오전":
        date_list[4] = "AM"
    else:
        date_list[4] = "PM"

    date_string = f'{date_list[0]}-{date_list[1]}-{date_list[2]} {date_list[4]} {date_list[5]}:{date_list[6]}'
    datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %p %I:%M')
    return datetime.datetime.timestamp(datetime_obj)

#{'정치' : 100, '경제' : 101, '사회' : 102, '문화' : 103, '세계' : 104, 'IT' : 105} 
# naver_news_code = {
#     '100' : [264, 265, 266, 267, 268],
#     '101' : [259, 258, 261, 771, 260],
#     '102' : [249, 250, 251, 254, 252],
#     '103' : [241, 239, 240, 237, 238],
#     '104' : [231, 232, 233, 234, 322],
#     '105' : [731, 226, 227, 230, 732],
# }
naver_news_code = {
    '100' : [265],
    # '101' : [259],
    # '102' : [249],
    # '103' : [239],
    # '104' : [231],
    # '105' : [226],
}

category_list = [key for key in naver_news_code.keys()]

def parse_naver():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
    
    news_info = []
    for category in category_list:
        scraped_date = datetime.datetime.today().strftime("%Y%m%d")
        for sub_category in naver_news_code[category]:
            # time.sleep(5)
            for num in range(1,2):
                # time.sleep(5)
                url = f'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={sub_category}&sid1={category}&date={scraped_date}&page={num}'
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')

                headline = soup.select("#main_content > div.list_body.newsflash_body > ul.type06_headline > li")
                # non_headline = soup.select("#main_content > div.list_body.newsflash_body > ul.type06 > li")

                news_uls = [headline]  # 총 20개의 기사 스크래핑 가능
                

                for news_ul in news_uls:
                    for news_li in news_ul:
                        try:
                            time.sleep(3)
                            category = soup.select_one("#snb > h2 > a").text
                            press = news_li.select_one("dl > dd > span.writing").text
                            preview_img = news_li.select_one("li > dl > dt.photo > a > img")['src']
                            title = news_li.select_one("dl > dt:nth-child(2) > a").text.strip()
                            ref = news_li.select_one("dl > dt:nth-child(2) > a")['href']
                            
                            # 기사 코드, 상세내용, 날짜 스크래핑
                            article_res = requests.get(ref, headers=headers)
                            article_soup = BeautifulSoup(article_res.text, 'html.parser')
                            print(title)
                            code = ref.split("aid=")[1]
                            content = article_soup.select_one("#articleBodyContents")  # 태그 타입임, str(content) 해줘야 함
                            date_str = article_soup.select_one("#main_content > div.article_header > div.article_info > div > span.t11").text
                        
                            data = {
                                'category' : category,
                                'press' : press,
                                'code' : code,
                                'preview_img' : preview_img,
                                'title' : title,
                                'content': str(content),
                                'date' : date_str,
                                'ref' : ref,
                            }
                            news_info.append(data)

                        except TypeError:
                            print('error')
                            pass

    return news_info


if __name__=='__main__':
    news_list = parse_naver()
    print(len(news_list))
    print("스크래핑 성공")
    # try:
    for news in news_list:
        date_list = news['date'].replace(".", " ").replace(":", " ").split(" ")
        time_obj = convert_datetime_to_timestamp(date_list)
        category = Category.objects.filter(name=news['category']).first()
        press = Press.objects.filter(name=news['press']).first()
        if not press:
            press = Press.objects.create(name=news['press'])
        
        article = Article.objects.filter(title=news['title']).first()
        if not article:
            
            if news['category'] == "생활/문화":
                category = Category.objects.filter(name='문화').first()
            
            if news['category'] == "IT/과학":
                category = Category.objects.filter(name='IT').first()
            
            if news['category'] == "세계":
                category = Category.objects.filter(name='국제').first()

            Article.objects.create(
                category=category,
                press=press,
                potal=Potal.objects.filter(name="네이버").first(),
                code=news['code'],
                preview_img=news['preview_img'],
                title=news['title'],
                content=news['content'],
                date=news['date'],
                ref=news['ref'],
                counted_at = 0,
                created_at=time_obj,
            )
            print("DB 넣기 성공")

    # except:
    #     print("DB 넣기 실패")
    #     pass



