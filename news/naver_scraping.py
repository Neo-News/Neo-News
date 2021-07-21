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


# 100 : 정치, 101: 경제, 102 : 사회, 103 : 생활/문화, 104 : 세계, 105 : IT/과학, 106 : X, 107 : 연예
# category_list = [100, 101, 102, 103, 104, 105, 107]
category_list = [103]
sub_category_list = [241, 239]

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

def parse_naver():
    news_info = []
    for category in category_list:
        scraped_date = datetime.datetime.today().strftime("%Y%m%d")
        for sub_category in sub_category_list:
            for num in range(1,2):
                url = f'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={sub_category}&sid1={category}&date={scraped_date}&page={num}'
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')

                headline = soup.select("#main_content > div.list_body.newsflash_body > ul.type06_headline > li")
                # non_headline = soup.select("#main_content > div.list_body.newsflash_body > ul.type06 > li")

                news_uls = [headline]  # 총 20개의 기사 스크래핑 가능

                for news_ul in news_uls:
                    for news_li in news_ul:
                        try:
                            time.sleep(1)
                            category = soup.select_one("#snb > h2 > a").text
                            print(category)
                            press = news_li.select_one("dl > dd > span.writing").text
                            preview_img = news_li.select_one("li > dl > dt.photo > a > img")['src']
                            title = news_li.select_one("dl > dt:nth-child(2) > a").text.strip()
                            ref = news_li.select_one("dl > dt:nth-child(2) > a")['href']
                            
                            # 기사 코드, 상세내용, 날짜 스크래핑
                            article_res = requests.get(ref, headers=headers)
                            article_soup = BeautifulSoup(article_res.text, 'html.parser')

                            code = ref.split("aid=")[1]
                            content = article_soup.select_one("#articleBodyContents")  # 태그 타입임, str(content) 해줘야 함
                            
                            date_str = article_soup.select_one("#main_content > div.article_header > div.article_info > div > span.t11").text
                            # date_list = date_str.replace(".", " ").replace(":", " ").split(" ")

                        except TypeError:
                            print('error')
                            pass               

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
                        print(data)
                        
                        news_info.append(data)
    return news_info



if __name__=='__main__':
    news_list = parse_naver()
    print("스크래핑 성공")
    # try:
    for news in news_list:
        press = Press.objects.filter(name=news['press']).first()
        if not press:
            press = Press.objects.create(name=news['press'])
        article = Article.objects.filter(title=news['title']).first()
        if not article:
            date_list = news['date'].replace(".", " ").replace(":", " ").split(" ")
            time_obj = convert_datetime_to_timestamp(date_list)
            Article.objects.create(
                category=Category.objects.filter(name=news['category']).first(),
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



