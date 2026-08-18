# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_api_keys():
    gemini_key = os.getenv("GEMINI_API_KEY")
    kakao_key = os.getenv("KAKAO_API_KEY")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("설정 방법: export GEMINI_API_KEY='your_key'")
        exit(1)
    
    if not kakao_key:
        print("❌ KAKAO_API_KEY 환경변수가 설정되지 않았습니다.")
        print("설정 방법: export KAKAO_API_KEY='your_key'")
        exit(1)
    
    return gemini_key, kakao_key