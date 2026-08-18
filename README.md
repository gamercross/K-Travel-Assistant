# Travel Planner 🌍

Google Gemini API와 Kakao Local API를 조합하여...

## 설치

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## API 키 설정

### macOS/Linux
\`\`\`bash
export GEMINI_API_KEY="your_key_here"
export KAKAO_API_KEY="your_key_here"
\`\`\`

### Windows PowerShell
\`\`\`powershell
$env:GEMINI_API_KEY="your_key_here"
$env:KAKAO_API_KEY="your_key_here"
\`\`\`

## 실행

\`\`\`bash
python travel_planner.py -date "2024-03-15"
\`\`\`

## 결과 확인

results/ 폴더에 생성된 파일 확인:
- \`YYYY-MM-DD_data.json\`: 원본 데이터
- \`YYYY-MM-DD_travel_plan.md\`: 최종 리포트

## ⚠️ 보안 주의사항

- **API 키를 코드에 직접 작성하지 마세요**
- **.env 파일은 .gitignore에 포함됩니다**
- 변수 이름을 공개해도, 값은 절대 공개하지 마세요