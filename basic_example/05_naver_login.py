"""
Date: 22.07.20
Description: 네이버(naver.com) 자동 로그인(auto login)
"""

# selenium lib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

user_id = 'id '
user_pw = 'pw'

# Get driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

""" 네이버 로그인 """
# 1. 네이버 이동
driver.get('https://naver.com')

# 2. 로그인 버튼 클릭
elem = driver.find_element(By.CLASS_NAME, 'link_login')
elem.click()

# 3. id, pw 입력
'''
driver.find_element(By.ID, 'id').send_keys(user_id)
driver.find_element(By.ID, 'pw').send_keys(user_pw)
'''

# 3. id 복사 붙여넣기
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
