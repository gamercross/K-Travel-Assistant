# travel_planner.py
import argparse
import json
import os
from datetime import datetime
from src.config import get_api_keys
from src.gemini_client import GeminiClient
from src.kakao_client import KakaoClient

def main():
    # CLI 파싱
    parser = argparse.ArgumentParser(description="국내 여행 추천 프로그램")
    parser.add_argument("-date", required=True, help="여행 날짜 (YYYY-MM-DD)")
    args = parser.parse_args()
    
    # 날짜 검증
    try:
        travel_date = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("❌ 날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)")
        exit(1)
    
    # API 키 확인
    gemini_key, kakao_key = get_api_keys()
    
    # 결과 저장 폴더
    os.makedirs("results", exist_ok=True)
    
    errors = []
    
    # [1/3] 1차 추천
    print("[1/3] 1차 추천 생성 중(LLM)...")
    gemini = GeminiClient(gemini_key)
    recommendation, err = gemini.get_travel_recommendation(args.date)
    
    if err:
        errors.append(err)
        print("❌ 추천 생성 실패. 재시도 중...")
        recommendation, err = gemini.get_travel_recommendation(args.date)
        if err:
            print("❌ 추천 생성 최종 실패")
            exit(1)
    
    print(f"  - 추천 지역: {recommendation['recommended_city']}")
    
    # [2/3] 맛집 검색
    print("[2/3] 맛집 검색 중(지도 API)...")
    kakao = KakaoClient(kakao_key)
    restaurants, err = kakao.search_restaurants(recommendation['recommended_city'])
    
    if err:
        errors.append(err)
        print(f"  - 경고: {err['message']}")
        restaurants = []
    else:
        print(f"  - 맛집 {len(restaurants)}곳 검색 완료")
    
    # [3/3] 최종 리포트
    print("[3/3] 최종 리포트 생성 중(LLM)...")
    report = gemini.generate_report(recommendation, restaurants)
    
    # 결과 저장
    date_str = args.date.replace("-", "")
    
    # JSON 저장
    result_data = {
        "date": args.date,
        "recommendation": recommendation,
        "restaurants": restaurants,
        "errors": errors
    }
    
    json_path = f"results/{args.date}_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    # Markdown 저장
    md_path = f"results/{args.date}_travel_plan.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n✅ 완료!")
    print(f"  - JSON: {json_path}")
    print(f"  - 리포트: {md_path}")

if __name__ == "__main__":
    main()