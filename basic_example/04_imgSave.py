"""
Date: 21.04.08
url: https://blog.naver.com/dsz08082/222302370266
- 여러 이미지 자동 저장
"""

# selenium ver. 3.141.0
from selenium import webdriver
import time
from urllib.request import urlretrieve
import os

# 이미지 저장용 폴더
search = "파이썬"
path = './images/' # 이미지 저장 폴더
if not os.path.isdir(path): # 없으면 새로 생성
    os.mkdir(path)

# 변수 설정
url = f"https://www.google.com/search?q={search}&source=lnms&tbm=isch"
img_path = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img'

# 드라이버 설정
driver = webdriver.Chrome("chromedriver")
driver.implicitly_wait(3)
driver.get(url)
driver.execute_script("window.scrollTo(0, 500")

# 이미지 자동 저장
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
cnt = 0
for index, img in enumerate(images):
	try:
		img.click()
		time.sleep(2)
		imgUrl = driver.find_element_by_xpath(img_path).get_attribute("src")

		if '?' in imgUrl:
			filetype = imgUrl[imgUrl.rfind('.'):imgUrl.rfind('?')]
		elif '.' in imgUrl:
			filetype = imgUrl[imgUrl.rfind('.'):]
		urlretrieve(imgUrl, path + str(index) + filetype)
		cnt += 1
	except Exception as e:
		print(f"Index: {index}, Passed")
		pass


driver.close()
print(f"Total CNT: {index}, Success CNT: {cnt}")
