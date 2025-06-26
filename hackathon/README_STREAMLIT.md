# 🤖 석주님 AI 챗봇 (Streamlit 버전)

기존의 CLI 기반 AI 챗봇을 웹 기반 Streamlit 애플리케이션으로 변환한 버전입니다.

## 📋 주요 기능

- 🌐 **웹 기반 인터페이스**: 브라우저에서 바로 사용 가능
- 💬 **실시간 채팅**: 스트리밍 응답으로 자연스러운 대화
- 📚 **대화 기록**: 세션 동안 대화 내용 저장
- 🎨 **사용자 친화적 UI**: 직관적이고 깔끔한 디자인
- ⚙️ **설정 옵션**: 사이드바에서 대화 기록 초기화 등

## 🚀 실행 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에 OpenAI API 키가 설정되어 있는지 확인:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Streamlit 앱 실행

#### 방법 A: 직접 실행
```bash
streamlit run streamlit_app.py
```

#### 방법 B: 실행 스크립트 사용
```bash
python run_streamlit.py
```

### 4. 브라우저 접속
- 자동으로 브라우저가 열리거나
- 수동으로 http://localhost:8501 접속

## 📁 파일 구조

```
hackathon/
├── main.py              # 기존 CLI 버전
├── util.py              # 공통 유틸리티
├── streamlit_app.py     # 새로운 Streamlit 앱
├── run_streamlit.py     # 실행 스크립트
├── requirements.txt     # 필요한 패키지 목록
└── README_STREAMLIT.md  # 이 파일
```

## 🔄 기존 버전과의 차이점

| 항목 | CLI 버전 (main.py) | Streamlit 버전 |
|------|-------------------|----------------|
| 인터페이스 | 터미널 | 웹 브라우저 |
| 대화 방식 | 일회성 질문 | 연속 대화 |
| 기록 관리 | 없음 | 세션 기록 |
| 사용성 | 개발자용 | 일반 사용자용 |
| 시각적 요소 | 텍스트만 | 이모지, 스타일링 |

## 🛠️ 추가 기능 아이디어

- 🎨 테마 변경 옵션
- 📊 대화 통계
- 💾 대화 내용 내보내기
- 🔧 모델 매개변수 조정
- 📝 시스템 프롬프트 수정 기능

## ⚠️ 주의사항

- OpenAI API 키가 필요합니다
- 인터넷 연결이 필요합니다
- API 사용량에 따라 비용이 발생할 수 있습니다

## 🐛 문제 해결

### 포트 충돌 시
```bash
streamlit run streamlit_app.py --server.port 8502
```

### 패키지 설치 문제 시
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```
