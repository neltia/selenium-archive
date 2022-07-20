"""
Date: 21.04.08
url: https://blog.naver.com/dsz08082/222302370266
- 이미지 찾기
"""

# selenium ver. 3.141.0
from selenium import webdriver
import time

search = "파이썬"
url = f"https://www.google.com/search?q={search}&source=lnms&tbm=isch"

driver = webdriver.Chrome("chromedriver")
driver.implicitly_wait(3)
driver.get(url)

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
img_path = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img'

cnt = 0
for img in images:
	try:
		img.click()
		time.sleep(2)
		imgUrl = driver.find_element_by_xpath(img_path).get_attribute("src")
		cnt += 1
		print(f"Index: {cnt}, 이미지 주소: {imgUrl}")
	except Exception as e:
		print(f"Index: {cnt}, Passed")
		pass

driver.close()
print("\nTotal CNT:", cnt)
