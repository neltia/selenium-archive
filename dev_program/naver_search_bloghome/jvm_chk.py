"""
main(step6)
형태소 분석을 위한 konlpy 라이브러리 사용을 위해 jvm 필요
"""

# jvm 확인을 위해 이 코드를 실행해주세요.
import platform
print(platform.architecture())

# 결과가 다음 같이 출력된다면
# ('64bit', 'WindowsPE')

# 다음 사이트에서 Windows x64 jdk를 다운로드 받아주세요.
# https://www.oracle.com/java/technologies/downloads/#java8

# 오라클 계정이 없다면 다음 사이트에서 Windows x64 jdk를 다운로드 받아주세요.
# https://github.com/portapps/oracle-jdk-portable/releases

# * jdk의 설치 경로도 환경변수에 추가해야 합니다.
