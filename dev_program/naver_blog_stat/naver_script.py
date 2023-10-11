"""
Date: 23.10.09
url: https://blog.naver.com/dsz08082/223232098414
- 네이버 로그인 -> 블로그 통계 캡처 -> 이미지 메일 전송
"""

# selenium lib
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
# mail send
import os
import smtplib
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

user_id = 'your id'
user_pw = 'your pw'
about_email = 'email addr for send'


# 네이버 로그인 함수
def login(driver):
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


# 메일 전송 함수
def mail_send(file_path):
    msg = MIMEMultipart()
    msg['From'] = f'{user_id}@naver.com'
    msg['To'] = about_email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(s=f'현재 시간 {user_id}의 블로그 통계', charset='utf-8')
    body = MIMEText('첨부된 파일을 확인해 주세요.', _charset='utf-8')
    msg.attach(body)

    files = list()
    files.append(file_path)

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    mailServer = smtplib.SMTP_SSL('smtp.naver.com')
    # 본인 계정, 비밀번호 사용
    mailServer.login(user_id, user_pw)
    mailServer.send_message(msg)
    mailServer.quit()
