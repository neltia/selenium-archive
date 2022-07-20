"""
Date: 22.07.20
Description: 현재 크롬 버전에 맞는 웹 드라이버 자동 다운로드
"""

# selenium lib
from selenium import webdriver
import chromedriver_autoinstaller
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

# Get driver and open url
driver = webdriver.Chrome(driver_path)
driver.get("https://google.com")
time.sleep(1)
driver.quit()

# # Check if chrome driver is installed or not & auto remove
if os.path.exists(folder_path):
    print(f"remove the chrome driver(ver: {folder_path})")
    shutil.rmtree(folder_path)
else:
    print(f"chrom driver is not insatlled: {driver_path}")
