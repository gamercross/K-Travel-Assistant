# src/gemini_client.py
import google.genai as genai
import json

class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def get_travel_recommendation(self, date_str):
        """
        date_str: "YYYY-MM-DD" 형식
        반환: {recommended_city, weather, events, reason}
        """
        prompt = f"""
당신은 한국 여행 전문가입니다.
날짜: {date_str}

아래 JSON 형식으로만 응답하세요 (다른 텍스트 없음):
{{
    "recommended_city": "도시명(예: 제주)",
    "weather": "해당 시기 날씨 요약",
    "events": ["축제1", "축제2"],
    "reason": "추천 근거 2-4문장"
}}
"""
        try:
            response = self.model.generate_content(prompt)
            # JSON 파싱
            json_str = response.text.strip()
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1].replace("json", "").strip()
            
            data = json.loads(json_str)
            return data, None
        except json.JSONDecodeError as e:
            return None, {"step": "recommendation", "type": "JSON_PARSE_ERROR", "message": str(e)}
        except Exception as e:
            return None, {"step": "recommendation", "type": "API_ERROR", "message": str(e)}
    
    def generate_report(self, recommendation, restaurants):
        """
        최종 리포트 생성 (Markdown)
        """
        restaurants_text = ""
        if restaurants:
            restaurants_text = "\n".join([f"- {r['name']} ({r['address']})" for r in restaurants])
        else:
            restaurants_text = "- 데이터 없음"
        
        prompt = f"""
아래 정보를 바탕으로 여행 리포트(Markdown)를 작성하세요.

추천 지역: {recommendation['recommended_city']}
이유: {recommendation['reason']}
날씨: {recommendation['weather']}
행사: {', '.join(recommendation['events'])}
맛집: {restaurants_text}

마크다운 형식으로 작성하되, 제목, 소제목, bullet list를 활용하세요.
1일 일정도 오전/오후/저녁으로 제안하세요.
"""
        response = self.model.generate_content(prompt)
        return response.text