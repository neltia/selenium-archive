# selenium lib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
# etc
from dotenv import load_dotenv
import pyperclip
import time
import os


# driver setting
def get_driver():
    # 드라이버 설정
    options = Options()
    user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Whale/3.23.214.10 Safari/537.36"
    options.add_argument(user_agent)
    # - 드라이버 시작
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)
    return driver


# 네이버 로그인 함수
def naver_login(driver, user_id, user_pw):
    # 1. 네이버 이동
    driver.get('https://naver.com')

    # 2. 로그인 버튼 클릭
    btn_class_name = 'MyView-module__link_login___HpHMW'
    elem = driver.find_element(By.CLASS_NAME, btn_class_name)
    elem.click()

    # 3. id 입력
    elem_id = driver.find_element(By.ID, 'id')
    elem_id.click()
    pyperclip.copy(user_id)
    elem_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 4. pw 복사 붙여넣기
    elem_pw = driver.find_element(By.ID, 'pw')
    elem_pw.click()
    pyperclip.copy(user_pw)
    elem_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 5. 로그인 버튼 클릭
    driver.find_element(By.ID, 'log.login').click()
    time.sleep(3)


# 네이버 톡톡에서 안 읽음으로 처리된 목록 가져오기
# * 읽음/안 읽음 처리된 톡톡을 선택 가능하게 설정
# 네이버 톡톡 리스트에서 각 "맞팬"과 "https://in.naver.com" 링크 파싱
def link_parsing_talktalk(driver, my_influencer_id):
    influencer_list = list()
    return influencer_list


# 따로 만든 파일에서 인플루언서 아이디 목록 가져오기
# 지원 파일: txt, excel
def link_parsing_file():
    influencer_list = list()
    return influencer_list


# 인플루언서 아이디 목록을 가져오는 함수
def get_influencer_list(driver, my_influencer_id, auto):
    # 자동으로 톡톡에 맞팬 요청을 신청하는 인플루언서에 한 해서,
    # 팬하기 요청을 수행하고 싶을 때
    if auto:
        influencer_list = link_parsing_talktalk(driver, my_influencer_id)
        return influencer_list

    # 수동으로 파일에다가 리스트를 나열한 것을 바탕으로
    # 팬하기 요청을 수행하고 싶을 때
    influencer_list = link_parsing_file()
    return influencer_list


# verfication: 이미 팬하기를 한 인플루언서인가?
def follow_verification(driver):
    home_div_class = "hm-component-homeCover-profile-btn"
    try:
        home_div_elem = driver.find_element(By.CLASS_NAME, home_div_class)
        home_text = home_div_elem.text
    except exceptions.NoSuchElementException:
        msg = "해당 인플루언서를 찾을 수 없습니다."
        print(msg)
        return -1

    if "팬하기" in home_text:
        return True
    else:
        return False


# 팬하기 자동화 수행
def influencer_follow(driver, influencer_list):
    follow_btn_class = "hm-component-homeCover-profile-btn"
    alert_div_class = "FanPopup__label_notice___iPdOs"
    close_btn_class = "FanPopup__button_close___rBmXm"

    for idx, influencer_id in enumerate(influencer_list):
        idx += 1
        if influencer_id.startswith("https://in.naver.com/"):
            influencer_id = influencer_id.split("/")[-1]

        page = f"https://in.naver.com/{influencer_id}"
        driver.get(page)
        time.sleep(1)

        print(idx, influencer_id)
        verify = follow_verification(driver)
        print(f"신규 팬하기 설정 대상: {verify}")

        # - 잘못된 질의 혹은 이미 팬하기가 되어있는 경우
        if verify == -1 or not verify:
            continue

        time.sleep(1)
        try:
            follow_elem = driver.find_element(By.CLASS_NAME, follow_btn_class)
            follow_elem.click()
            print("팬하기 완료")

            disable_elem = driver.find_element(By.CLASS_NAME, alert_div_class)
            disable_elem.click()
            print("알림 취소 설정 완료")

            close_elem = driver.find_element(By.CLASS_NAME, close_btn_class)
            close_elem.click()
            print("창 닫기 완료")
        except exceptions.NoSuchElementException:
            print("네이버의 인플루언서 홈 정보가 변경되었습니다. 프로그램 버전 업데이트가 필요합니다.")
            continue


# 메인 함수
def main():
    # init
    load_dotenv(verbose=True)
    driver = get_driver()

    # naver login
    user_id = os.environ.get("naver_id")
    user_pw = os.environ.get("naver_pw")
    naver_login(driver, user_id, user_pw)

    # in.naver.com list
    my_influencer_id = os.environ.get("my_influencer_id")
    list_auto = os.environ.get("list_auto")
    influencer_list = get_influencer_list(driver, my_influencer_id, list_auto)

    # follow repeat in list
    influencer_follow(driver, influencer_list)


if __name__ == "__main__":
    main()
