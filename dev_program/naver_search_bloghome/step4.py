"""
step4. step3에서 가져온 url 목록을 활용해 글 내용을 가져옵니다.
"""
# selenium lib
# - selenium 라이브러리란?
# -- 제가 블로그에 작성한 셀레니움 글 목록 읽기를 추천드립니다.
# -- (https://blog.naver.com/dsz08082/222298630856)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common import exceptions
# else python lib
import time

# 기본 변수 설정
# - 검색할 단어
keyword = "넬티아"
# - 검색 수
end_page = 5
# - 블로그 url을 저장하기 위한 변수
url_list = []
# - 블로그 글 내용을 저장하기 위한 변수
all_content = ""

# 셀레니움 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 블로그 검색 및 # 반복문을 사용해 페이지 링크 로딩 반복
for page_num in range(1, end_page):
    search_link = f"https://section.blog.naver.com/Search/Post.nhn?pageNo={page_num}&rangeType=ALL&orderBy=sim&keyword={keyword}"

    # - 페이지를 driver.get()으로 불러올 건데, 로딩 시간을 최대 2초까지 기다려줘
    driver.implicitly_wait(2)
    # - 현재 검색 URL을 불러와줘
    driver.get(search_link)

    # 너무 빠르게 하면 크롤링 방지로 인해 오류가 생길 수 있으니
    # 다음 페이지로 넘어갈 때마다 대기 시간을 둠
    time.sleep(0.5)

    # 각 블로그 게시글의 제목의 위치를 가져옴
    for j in range(1, 3):
        # xpath 관련 상세: https://blog.naver.com/dsz08082/222299225296
        xpath_title = '/html/body/ui-view/div/main/div/div/section/div[2]/div['+str(j)+']/div/div[1]/div[1]/a[1]'
        # xpath를 사용해 전체 제목들을 불러오고
        titles = driver.find_element(By.XPATH, xpath_title)
        # HTML에서 링크 값에 해닫하는 href 속성을 가져옴
        blog_link = titles.get_attribute('href')
        # 링크를 리스트 변수에 추가
        url_list.append(blog_link)
print("url data crawling end.")
print(url_list)

# 수집한 각 블로그로 이동해서 내용 가져오기
for blog_link in url_list:
    # 블로그 게시글로 이동
    driver.get(blog_link)
    # iframe 태그를 사용해 HTML 태그가 분리되어 있어 바로 해당 내용을 가져올 수 없음
    # switch_to.frame()을 사용한 프레임 전환 필요
    driver.switch_to.frame('mainFrame')

    # css로 글 내용 가져와 저장
    # - 구버전 블로그 에디터
    content_div_id = "postViewArea"
    # - 신버전 블로그 에디터
    content_css_selector = ".se-component.se-text.se-l-default"

    try:
        content = driver.find_element(By.ID, content_div_id)
        all_content += content.text
    except exceptions.NoSuchElementException:
        content = driver.find_element(By.CSS_SELECTOR, content_css_selector)
        all_content += content.text
print("text data crawling end.")
print(all_content)

# 웹 드라이버 종료 시 3초 기다렸다 종료
time.sleep(3)
