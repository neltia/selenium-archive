"""
Date: 23.10.09
url: https://blog.naver.com/dsz08082/223232098414
- 네이버 로그인 -> 블로그 통계 캡처 -> 이미지 메일 전송
"""

# selenium lib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# 로그인 함수
from naver_script import login
# 이메일 함수
from naver_script import mail_send
# else
import time, os
from datetime import datetime


# 드라이버 설정
options = Options()
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36"
options.add_argument(user_agent)
# - 드라이버 시작
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(5)

# 네이버 로그인
login(driver)

# 블로그 통계 확인
blog_id = "your naver blog id"
blog_url = f"https://admin.blog.naver.com/{blog_id}/stat/today"
driver.get(blog_url)
time.sleep(1)

# 화면 캡처 대상 디렉터리가 없으면 생성
output_dir = "img/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 현재 화면 캡처
now_time = datetime.today().strftime("%Y-%m-%d_%Hh")
output_name = f'{now_time}-{blog_id}_Blog.png'
driver.save_screenshot(f"{output_dir}/{output_name}")

# 메일 전송
mail_send(f"{output_dir}/{output_name}")

# 캡처한 이미지 삭제
os.remove(f"{output_dir}/{output_name}")
