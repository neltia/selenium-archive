"""
sele_nblog.py
date. 22.07.18
by. @neltia / dsz08082@naver.com
"""
# selenium lib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
from pytz import timezone
from datetime import datetime
import sys

# driver setting
options = Options()
# - user agent
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36"
options.add_argument(user_agent)
# - headless: 크롤링 시 웹 드라이버의 브라우저가 화면에 열리지 않고 백그라운드로 진행
options.add_argument("headless")
# - 드라이버 수행
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(3)

# 필요한 기본 정보
# - 이웃 목록을 가져올 사용자 아이디
blogger_id = "dsz08082"
# - 이웃 수
subscriber_cnt = 1742

# 22.07.19 기준 이웃수 1742
# 이웃 목록 페이지 수 20*87+2 = 1742//20+n
idx_rng = subscriber_cnt // 20 + 1

# data parsing
blog_url_list = []
blogger_name_list = []
for idx in range(1, idx_rng+1):
    get_url = f"https://section.blog.naver.com/connect/ViewMoreFollowers.naver?blogId={blogger_id}&currentPage={idx}"
    driver.get(get_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    link_list = soup.find_all('a', class_="buddy_name")
    for link in link_list:
        blog_url = link["href"].strip()
        blogger_name = link.text.strip()

        blog_url_list.append(blog_url)
        blogger_name_list.append(blogger_name)

    print(f"{idx} page completed")
    time.sleep(0.5)
driver.quit()

# pandas의 Dataframe을 활용하여 데이터 파싱
pre_dict = {'blogger': blogger_name_list, 'blog_url': blog_url_list}
df = pd.DataFrame(pre_dict)
df["mail_address"] = [f"{url.split('/')[-1]}@naver.com" for url in df["blog_url"]]
df.index += 1

# export excel
now_date = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d')
df.to_excel(f"blog_{blogger_id}_{now_date}.xlsx")
sys.exit()
