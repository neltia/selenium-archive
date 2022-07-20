"""
Date: 22.07.20
Description: 현재 크롬 버전에 맞는 웹 드라이버 자동 다운로드
"""

# selenium lib
from selenium import webdriver
import chromedriver_autoinstaller
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
import time

# current chrome version
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
folder_path = f'./{chrome_ver}'
driver_path = f'./{chrome_ver}/chromedriver.exe'

# Check if chrome driver is installed or not & auto install
if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

# Get driver
driver = webdriver.Chrome(driver_path)
"""
Get driver: DeprecationWarning: executable_path has been deprecated Warning 해결
셀레니움 4버전부터 별도 크롬 웹 드라이버 없이 현재 운영체제에 설치된 크롬 브라우저 사용 설정 권장
"""
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# open url
driver.get("https://google.com")
time.sleep(1)
driver.quit()

# # Check if chrome driver is installed or not & auto remove
if os.path.exists(folder_path):
    print(f"remove the chrome driver(ver: {folder_path})")
    shutil.rmtree(folder_path)
else:
    print(f"chrom driver is not insatlled: {driver_path}")
