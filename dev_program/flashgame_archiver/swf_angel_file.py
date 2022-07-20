"""
Date: 20.12.29
Description:
의뢰를 받고 플래시 게임이 곧 사라지니 swf 파일을
다수 다운로드하는 프로그램 제작 및 전달
"""

# Call Lib
from bs4 import BeautifulSoup # HTML 파싱 라이브러리
import requests # 웹 통신 라이브러리
import urllib.request # 웹 통신 라이브러리
from selenium import webdriver # 웹 브라우저를 띄워서 자바스크립트 동작된 상태로 크롤링
import time # 시간 대기
import random # 랜덤

# Var
rank_list = []

# url settings
main_url = "http://fg.gameangel.com" # 게임 엔젤 메인
base_url = "http://pds.gameangel.com/@files/gamefile/game_flash" # 게임 엔젤 플래시 저장 경로
top_url = "http://fg.gameangel.com/?dirname=top100&top_cgroup=game_flash" # 탑 100 페이지
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
# 헤더 설명 : https://blog.naver.com/dsz08082/222092533560

# rank_list
res = requests.get(top_url, headers = headers)
soup = BeautifulSoup(res.content, 'html.parser')
rank_data = soup.find("ul", {"class" : "game_list typ_rank"})
for item in rank_data:
	try:
		rank_list.append(item.find('a').get("href")) # 탑 100 플래시 게임 링크 추가
	except:
		pass

# swf link find
driver = webdriver.Firefox(executable_path="geckodriver.exe") # 파이어폭스 브라우저를 띄움

for inverse in range(len(rank_list)):
	r = random.randint(1, 2)
	time.sleep(r)
	driver.get(main_url + rank_list[inverse]) # 띄운 브라우저는 각 플래시 게임으로 이동
	driver.implicitly_wait(5) # 최대 5초까지 정상 페이지를 위해 대기
	play_button = "/html/body/div[2]/div[2]/div[1]/div[1]/ul/li[3]/a" # 버튼 경로

	try: # 오류 페이지면 패스
		driver.find_element_by_xpath(play_button).click() # 새 창 띄움

		driver.switch_to_window(driver.window_handles[1]) # 띄운 창으로 이동
		r = random.randint(1, 3)
		time.sleep(r)
		strs = str(driver.current_url) # 현재 페이지 주소 저장

		try: # 경로가 지정한 패턴과 다르면 패스
			s = "data_url" # 찾을 값
			p = strs.index(s) # 주소에서 값이 위치한 곳을 골라
			data = strs[p:].split("&") # 슬라이싱
			plus_url = data[0].split("=")[1] + "/" + data[1].split("=")[1] # 주소/파일이름

			url = base_url + plus_url # 저장할 플래시 저장소의 좌표
			r = random.randint(1, 2)
			time.sleep(r)
			req = requests.get(url, allow_redirects=True) # swf 파일 페이지를 가져와
			open(data[1].split("=")[1], 'wb').write(req.content) # 저장
		except:
			pass
	except:
		print(inverse)
		pass

	driver.close() # 끝나면 현재 페이지 닫고
	driver.switch_to_window(driver.window_handles[0]) # 다시 화면 전환
