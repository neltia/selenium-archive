import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import re
import pandas as pd


URL = "https://www.google.co.kr/maps/place/%EC%B9%B4%ED%8E%98+%EC%A0%95%EC%9B%94/data=!4m8!3m7!1s0x357ca3f6d10624bd:0x39a0e4a2088ea588!8m2!3d37.5036192!4d127.0286107!9m1!1b1!16s%2Fg%2F11h1g3jpfh?entry=ttu"
# URL = "https://www.google.co.kr/maps/place/%EC%A0%84%EC%A3%BC%EC%8B%9D%EB%8B%B9/data=!4m8!3m7!1s0x357ca3ed58bb036b:0xfcf83b20533d7294!8m2!3d37.5192691!4d127.0298639!9m1!1b1!16s%2Fg%2F1q5bscw23?entry=ttu"
DriverLocation = r"C:\Users\hy\AppData\Local\Programs\Python\Python312\chromedriver.exe"


def get_data(driver):
    print('데이터 가져오는 중...')

    # 리뷰 내용이 긴 경우 '자세히'버튼을 눌러 내용 전체 보기
    # - 자세히 버튼
    # more_elements = driver.find_elements(By.XPATH, '//*[@id="ChZDSUhNMG9nS0VJQ0FnSUMxbkxxTllBEAE"]/span[2]/button')
    more_elem_xpath = "//button[contains(text(),'자세히')]"
    more_elements = driver.find_elements(By.XPATH, more_elem_xpath)
    more_elem_cnt = len(more_elements)
    for _ in range(more_elem_cnt):
        more_element = driver.find_element(By.XPATH, more_elem_xpath)
        try:
            more_element.click()
        except ElementNotInteractableException:
            continue
        time.sleep(1)
    print("자세히 버튼 처리 완료")

    # 리뷰 내용 수집 부분
    time.sleep(0.2)
    parent_class = "jJc9Ad"
    name_text_class = "d4r55"
    review_text_class = "wiI7pd"
    lst_data = list()
    parent_elements = driver.find_elements(By.CLASS_NAME, parent_class)
    about_total_cnt = len(parent_elements)
    print(f"about total cnt: {about_total_cnt}")
    for idx, parent_elem in enumerate(parent_elements):
        per = about_total_cnt * idx / 100.0
        print(f"{per:.2f}%", end="\r")
        try:
            nickname_elem = parent_elem.find_element(By.CLASS_NAME, name_text_class)
            review_elem = parent_elem.find_element(By.CLASS_NAME, review_text_class)
        except NoSuchElementException:
            continue

        name = nickname_elem.text
        review_text = review_elem.text
        lst_data.append([name, review_text])

    print("데이터 수집 완료:")
    return lst_data


def get_total_review_cnt(driver):
    review_cnt_xpath = "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]"
    review_cnt_xpath2 = "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]"

    # result_element = driver.find_element(By.CLASS_NAME, 'fontBodySmall')
    try:
        result_element = driver.find_element(By.XPATH, review_cnt_xpath)
    except NoSuchElementException:
        result_element = driver.find_element(By.XPATH, review_cnt_xpath2)
    result = result_element.text
    print(result)

    pat = r"\d+"
    review_count = int(re.search(pat, result).group())
    return review_count


def scroll_to_bottom(driver, cnt):
    print('scrolling to bottom...')
    # Scroll to the bottom of the page

    sidebar_xpath = "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]"
    for _ in range(cnt):
        sidebar_elem = driver.find_element(By.XPATH, sidebar_xpath)
        sidebar_elem.send_keys(Keys.END)
        time.sleep(1)  # Wait for content to load


def write_to_xlsx(data):
    print('write to excel...')
    cols = ["name", "comment"]
    df = pd.DataFrame(data, columns=cols)
    df.to_excel('out.xlsx', index=False)


if __name__ == "__main__":
    print('starting...')

    # driver setting
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    DriverPath = DriverLocation
    service = Service(DriverPath)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # page load
    driver.get(URL)
    time.sleep(5)

    # review count
    total_review_cnt = get_total_review_cnt(driver)

    # Scroll to the bottom of the page
    scroll_cnt = total_review_cnt // 10 + 1
    scroll_to_bottom(driver, scroll_cnt)

    data = get_data(driver)
    driver.close()

    write_to_xlsx(data)
    print('completed')
