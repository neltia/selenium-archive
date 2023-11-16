"""
search_view_tab.py:
1. 네이버 검색창 뷰 탭에서 키워드 검색
2. konlpy 형태소 처리
3. 빈도 그래프 & 워드클라우드

* 연관 naver_search_bloghome/step6.py
- 네이버 블로그 검색 창에서 키워드로 블로그 글 검색
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
from bs4 import BeautifulSoup
# konlpy
# - konlpy 개념: https://blog.naver.com/dsz08082/221556111946
# - Twitter(Okt)로 한글 형태소 분석: https://blog.naver.com/dsz08082/222573153664
from konlpy.tag import Okt
from nltk import Text
# graph
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud
# else python lib
import time


# 셀레니움 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# 함수: 검색 결과에 해당하는 블로그/카페 주소 목록을 변수에 저장
def search_url_data(keyword, end_data_num):
    url_list = []

    # 네이버 뷰 탭 전체 기준 검색 링크
    search_link = f"https://search.naver.com/search.naver?where=view&sm=tab_jum&query={keyword}"

    # - 페이지를 driver.get()으로 불러올 건데, 로딩 시간을 최대 2초까지 기다려줘
    driver.implicitly_wait(2)
    # - 현재 검색 URL을 불러와줘
    driver.get(search_link)

    # 너무 빠르게 하면 크롤링 방지로 인해 오류가 생길 수 있으니
    # 다음 페이지로 넘어갈 때마다 대기 시간을 둠
    time.sleep(0.5)

    # 각 블로그 URL을 가져옴
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "lxml")
    # link_class_name = "total_wrap api_ani_send"  (23.10.24 이전 네이버 뷰 탭 검색 목록 CLASS 이름)
    link_class_name = "title_area"
    search_result_list = soup.find_all("div", attrs={"class": link_class_name})

    for search_result in search_result_list:
        # HTML에서 링크 값에 해닫하는 href 속성을 가져옴
        url_link = search_result.a["href"]

        # 링크를 리스트 변수에 추가
        url_list.append(url_link)

    # 수집한 url의 수가 정한 한도 값보다 크다면 뒤에 수집한 링크는 제거
    if len(url_list) > end_data_num:
        url_list = url_list[:end_data_num]

    print(f"전체 수집 url 수: {len(url_list)}")
    return url_list


# 함수: 수집한 각 블로그/카페로 이동해서 내용 가져오기
def data_parsing(url_list):
    # - 글 내용을 저장하기 위한 변수
    text_data = ""
    chk_url_cnt = 0

    for url_link in url_list:
        # url 분석 시작
        print(f"{url_link} - carwling progress")

        # 게시글로 이동
        driver.get(url_link)

        # iframe 태그를 사용해 HTML 태그가 분리되어 있어 바로 해당 내용을 가져올 수 없음
        # switch_to.frame()을 사용한 프레임 전환 필요
        # - 가져온 주소가 블로그 글인 경우
        # 2023년 기준 네이버 블로그의 메인 iframe 값은 mainFrame
        if url_link.startswith("https://blog.naver.com"):
            url_type = "blog"
            driver.switch_to.frame('mainFrame')

        # - 가져온 주소가 카페 글인 경우
        # 2023년 기준 네이버 카페의 메인 iframe 값은 cafe_main
        elif url_link.startswith("https://cafe.naver.com"):
            url_type = "cafe"
            driver.switch_to.frame('cafe_main')

        # - 가져온 주소가 네이버 포스트인 경우
        elif url_link.startswith("https://post.naver.com"):
            content_css_selector = ".se_component_wrap.sect_dsc.__se_component_area"
            try:
                content = driver.find_element(By.CSS_SELECTOR, content_css_selector)
                text_data += content.text
                chk_url_cnt += 1
                continue
            except exceptions.NoSuchElementException:
                print("글 내용 확인 중 오류가 발생했습니다. 해당 글을 건너뜁니다.")
                continue

        # css로 글 내용 가져와 저장
        # - 구버전 블로그 에디터
        content_div_id = "postViewArea"
        # - 신버전 블로그 에디터
        content_css_selector = ".se-component.se-text.se-l-default"

        # 구버전 블로그/카페 에디터의 경우
        try:
            content = driver.find_element(By.ID, content_div_id)
            text_data += content.text
            chk_url_cnt += 1
        # 신버전 블로그/카페 에디터의 경우
        except exceptions.NoSuchElementException:
            try:
                content = driver.find_element(By.CSS_SELECTOR, content_css_selector)
                chk_url_cnt += 1
            except exceptions.NoSuchElementException:
                if url_type == "cafe":
                    print("카페에 가입해야만 볼 수 있는 게시글입니다.")
                else:
                    print("글 내용 확인 중 오류가 발생했습니다. 해당 글을 건너뜁니다.")
                continue
            text_data += content.text

    print(f"데이터 추가 완료 url 수: {chk_url_cnt}")
    return text_data


# 트위터에서 만든 소셜 분석을 위한 형태소 분석기 Okt 사용
def morpheme_parsing(text_data):
    # 트위터에서 만든 소셜 분석을 위한 형태소 분석기 Okt 사용
    okt = Okt()
    myList = okt.pos(text_data, norm=True, stem=True) # 모든 형태소 추출
    myList_filter = [x for x, y in myList if y in ['Verb']] # 추출된 값 중 동사만 추출
    okt_parsing_text = Text(myList_filter, name="Okt")
    return okt_parsing_text.vocab()


# matplotlib 라이브러리로 막대 그래프, wordcloud 모듈로 워드클라우드 생성
def draw_graph(okt_parsing_text):
    # font 설정
    font_location = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)

    # 그래프 x, y 라벨 설정
    plt.xlabel("동사")
    plt.ylabel("빈도")

    # 그래프에서 x, y 값을 설정
    wordInfo = dict()
    for tags, counts in okt_parsing_text.most_common(50):
        if len(str(tags)) > 1:
            wordInfo[tags] = counts

    values = sorted(wordInfo.values(), reverse=True)
    keys = sorted(wordInfo, key=wordInfo.get, reverse=True)

    # 그래프 값 설정
    plt.bar(range(len(wordInfo)), values, align='center')
    plt.xticks(range(len(wordInfo)), list(keys), rotation='vertical')
    plt.show()

    # wordCloud 출력
    wc = WordCloud(width=1000, height=600, background_color="white", font_path=font_location, max_words=50)
    plt.imshow(wc.generate_from_frequencies(okt_parsing_text))
    plt.axis("off")
    plt.show()
    return


def main():
    # - 검색할 단어
    keyword = "네이버 카페"
    # - 그래프에 반영하는 수집할 최대 데이터 개수 (기본 최대 41개)
    end_data_num = 7

    url_list = search_url_data(keyword, end_data_num)
    print("url data crawling end.")

    text_data = data_parsing(url_list)
    print("text data crawling end.")

    okt_parsing_text = morpheme_parsing(text_data)
    print("okt parsing success.")

    draw_graph(okt_parsing_text)

    # 웹 드라이버 종료 시 3초 기다렸다 종료
    time.sleep(3)


main()
