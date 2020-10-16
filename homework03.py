import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
chart = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
# body-content > div.newest-list > div > table > tbody > tr # 전체
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number # 순위
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis # 제목
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis # 가수

# 차트 반복문 돌리기
for rank in chart:
    rank_tag = rank.select_one('td.number')
    if rank_tag is not None:
        number = rank.select_one('td.number').text[0:2].strip()
        title = rank.select_one('td.info > a.title.ellipsis').text.strip()
        singer = rank.select_one('td.info > a.artist.ellipsis').text
        doc = {
            'number' : number,
            'title' : title,
            'artists' : singer
        }
        print(number, title, singer)#doc에 넣고 출력하면 순서가 꼬이는데 이건 왜 그런 것인가
        db.chart.insert_one(doc)