"""
Date: 21.04.06
url: https://blog.naver.com/dsz08082/222299225296
"""

# selenium ver. 3.141.0
from selenium import webdriver

driver = webdriver.Chrome("chromedriver")
driver.get("https://www.google.com")

input_box = driver.find_element_by_name("q")
input_box.send_keys("python")
input_box.submit()
