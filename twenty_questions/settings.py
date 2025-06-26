"""
설정 파일
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 모델 설정
LLM_MODEL = "gpt-4o-mini"  # 더 저렴한 모델 사용
EMBEDDING_MODEL = "text-embedding-3-small"

# 게임 설정
MAX_QUESTIONS = 20
SUBJECTS_POOL = [
    # 동물
    "사자", "호랑이", "코끼리", "기린", "펭귄", "돌고래", "독수리", "나비", "개미", "고양이",
    
    # 사물
    "컴퓨터", "자동차", "피아노", "책", "시계", "카메라", "우산", "안경", "휴대폰", "자전거",
    
    # 음식
    "피자", "햄버거", "초밥", "파스타", "아이스크림", "케이크", "치킨", "라면", "김치", "빵",
    
    # 자연
    "태양", "달", "바다", "산", "강", "나무", "꽃", "구름", "별", "무지개",
    
    # 장소
    "학교", "병원", "도서관", "공원", "영화관", "박물관", "카페", "식당", "은행", "마트"
]

# 메모리 설정
MEMORY_NAMESPACE = "twenty_questions_game"
EMBEDDING_DIMENSIONS = 1536
