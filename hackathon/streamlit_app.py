import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 환경 변수 로드
load_dotenv()

# Streamlit 페이지 설정
st.set_page_config(
    page_title="석주님 AI 챗봇",
    page_icon="🤖",
    layout="wide"
)

# 제목
st.title("🤖 석주님 AI 챗봇")
st.markdown("---")


# OpenAI API 키 확인
@st.cache_resource
def initialize_model():
    """모델 초기화"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY가 설정되지 않았습니다!")
        st.stop()

    model = ChatOpenAI(model="gpt-3.5-turbo")

    template = """
            너는 이제부터 무조건 석주님을 붙이고 말끝에는 뀨~!를 붙여 대답을 해줘야해
            
            질문:
            {question}
            """

    prompt = PromptTemplate.from_template(template)
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    return chain


# 모델 초기화
chain = initialize_model()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바
with st.sidebar:
    st.header("📋 설정")

    # 대화 기록 초기화 버튼
    if st.button("🗑️ 대화 기록 초기화", type="secondary"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ 정보")
    st.markdown("- 모델: GPT-3.5 Turbo")
    st.markdown("- 특징: 모든 답변에 '석주님' 호칭 사용")

# 메인 채팅 영역
st.header("💬 채팅")

# 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # 스트리밍 응답
            with st.spinner("생각 중..."):
                response_stream = chain.stream({"question": prompt})

                for chunk in response_stream:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                # 마지막에 커서 제거
                message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {str(e)}")
            full_response = "죄송합니다, 석주님. 오류가 발생했습니다."
            message_placeholder.markdown(full_response)

    # AI 응답을 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 하단 정보
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Made with ❤️ using Streamlit & LangChain
    </div>
    """,
    unsafe_allow_html=True
)
