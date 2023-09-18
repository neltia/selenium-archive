"""
step2. 셀레니움 실행 가능 환경인지 확인합니다.
- 셀레니움은 실제로 브라우저를 열어서 데이터를 가져오기 위한 크롤링 라이브러리입니다.
- 자세한 설명은 주석을 참고해주세요.
"""
# selenium lib
# - selenium 라이브러리란?
# -- 제가 블로그에 작성한 셀레니움 글 목록 읽기를 추천드립니다.
# -- (https://blog.naver.com/dsz08082/222298630856)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# else python lib
import time

# 기본 변수 설정
keyword = "넬티아"
search_link = f"https://section.blog.naver.com/Search/Post.nhn?pageNo=0&rangeType=ALL&orderBy=sim&keyword={keyword}"

# 셀레니움 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 검색 링크 호출
driver.implicitly_wait(3)
driver.get(search_link)

# 웹 드라이버 종료 시 3초 기다렸다 종료
time.sleep(3)
