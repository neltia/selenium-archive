"""
main(step6)
형태소 분석을 위한 konlpy 라이브러리 설치 여부 확인 테스트
"""
from konlpy.tag import Okt

okt = Okt()
result = okt.morphs("안녕하세요. 컴퓨터를 사러 왔습니다.")
print(result)
