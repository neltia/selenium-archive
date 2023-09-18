"""
main(step6):
1. 네이버 블로그 홈에서 키워드 검색
2. konlpy 형태소 처리
3. 빈도 그래프 & 워드클라우드

실행 전 준비사항
- 라이브러리 설치
pip install konlpy nltk matplotlib wordcloud
- jvm 구성 필요
jvm_chk.py 파일 확인
- konlpy 라이브러리 사용 준비 확인
konlpy_chk.py 파일 실행 여부 확인
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


# 함수: 블로그에서 데이터를 가져와 변수에 저장
def search_blog_data(keyword, end_page):
    url_list = []

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
    return url_list


# 함수: 수집한 각 블로그로 이동해서 내용 가져오기
def data_parsing(url_list):
    # - 블로그 글 내용을 저장하기 위한 변수
    text_data = ""

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
            text_data += content.text
        except exceptions.NoSuchElementException:
            content = driver.find_element(By.CSS_SELECTOR, content_css_selector)
            text_data += content.text
    return text_data


# 트위터에서 만든 소셜 분석을 위한 형태소 분석기 Okt 사용
def morpheme_parsing(text_data):
    # 트위터에서 만든 소셜 분석을 위한 형태소 분석기 Okt 사용
    okt = Okt()
    # - 모든 형태소 추출
    myList = okt.pos(text_data, norm=True, stem=True)
    # - 추출된 값 중 동사만 추출
    myList_filter = [x for x, y in myList if y in ['Verb']]
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
    keyword = "넬티아"
    # - 검색 수
    end_page = 5

    url_list = search_blog_data(keyword, end_page)
    print("url data crawling end.")

    text_data = data_parsing(url_list)
    print("text data crawling end.")

    okt_parsing_text = morpheme_parsing(text_data)
    print("okt parsing success.")

    draw_graph(okt_parsing_text)

    # 웹 드라이버 종료 시 3초 기다렸다 종료
    time.sleep(3)


main()
