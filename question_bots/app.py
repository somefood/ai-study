"""
간단한 메모리 챗봇 - Streamlit + LangMem
"""
import streamlit as st
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")

try:
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent
    from langgraph.store.memory import InMemoryStore
    from langmem import create_manage_memory_tool, create_search_memory_tool
except ImportError as e:
    st.error(f"필요한 패키지가 설치되지 않았습니다: {e}")
    st.stop()


# Streamlit 페이지 설정
st.set_page_config(
    page_title="간단한 메모리 챗봇",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 간단한 메모리 챗봇")
st.markdown("LangMem을 사용해서 당신의 질문과 대화를 기억하는 챗봇입니다!")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    user_name = st.text_input("사용자 이름", value="사용자", key="user_name")
    
    if st.button("🗑️ 메모리 초기화"):
        # 세션 상태 초기화
        for key in ['messages', 'agent', 'store']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("메모리가 초기화되었습니다!")
        st.rerun()


@st.cache_resource
def create_agent():
    """메모리 에이전트 생성 (캐싱)"""
    try:
        # 메모리 저장소 설정
        store = InMemoryStore(
            index={
                "dims": 1536,
                "embed": "openai:text-embedding-3-small",
            }
        )
        
        # LLM 초기화
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=OPEN_AI_KEY)
        
        # 메모리 도구 생성
        manage_memory_tool = create_manage_memory_tool(namespace=("chat_memory",))
        search_memory_tool = create_search_memory_tool(namespace=("chat_memory",))
        memory_tools = [manage_memory_tool, search_memory_tool]
        
        # 시스템 프롬프트 (더 간단하고 명확하게)
        system_prompt = """당신은 사용자의 정보를 기억하는 AI 어시스턴트입니다.

        주요 역할:
        1. 사용자가 개인 정보를 말하면 manage_memory 도구로 저장하세요
        2. 사용자가 이전 정보를 묻거나 관련 대화를 할 때 search_memory 도구로 검색하세요
        3. 친근하고 자연스러운 대화를 유지하세요
        
        저장할 정보 예시:
        - 이름, 나이, 직업
        - 취미, 관심사
        - 좋아하는 것/싫어하는 것
        - 목표, 계획
        - 일상적인 습관
        
        항상 도구를 적극 활용하여 개인화된 대화를 제공하세요."""

        # 에이전트 생성 - 시스템 프롬프트를 직접 전달
        agent = create_react_agent(
            llm,
            tools=memory_tools,
            store=store,
            prompt=system_prompt
        )
        
        return agent, store
        
    except Exception as e:
        st.error(f"에이전트 초기화 실패: {e}")
        return None, None


# 에이전트 초기화
if 'agent' not in st.session_state:
    with st.spinner("🤖 챗봇을 초기화하는 중..."):
        agent, store = create_agent()
        if agent:
            st.session_state.agent = agent
            st.session_state.store = store
            st.success("✅ 챗봇이 준비되었습니다!")
        else:
            st.error("❌ 챗봇 초기화에 실패했습니다.")
            st.stop()

# 메시지 히스토리 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": f"안녕하세요 {user_name}님! 저는 당신과의 대화를 기억할 수 있는 메모리 챗봇입니다. 개인 정보를 알려주시면 기억해두겠습니다! 🤖"
        }
    ]

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if user_input := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 어시스턴트 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            try:
                # 사용자 ID 설정 (메모리 도구에서 사용)
                config = {
                    "configurable": {
                        "user_id": user_name,
                        "thread_id": f"thread_{user_name}"
                    }
                }
                
                # 에이전트 호출 - 올바른 형식으로
                response = st.session_state.agent.invoke(
                    {"messages": [{"role": "user", "content": user_input}]},
                    config=config
                )
                
                # 응답 추출
                if response and "messages" in response and len(response["messages"]) > 0:
                    # 마지막 AI 메시지 가져오기
                    assistant_message = response["messages"][-1].content
                else:
                    assistant_message = "죄송합니다. 응답을 생성하는데 문제가 발생했습니다."
                
                st.markdown(assistant_message)
                
                # 메시지 히스토리에 추가
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_message
                })
                
            except Exception as e:
                error_message = f"오류가 발생했습니다: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"죄송합니다. 처리 중 오류가 발생했습니다. 다시 시도해주세요."
                })

# 하단 정보
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("💬 **대화 기능**\n- 자연스러운 대화\n- 질문과 답변")

with col2:
    st.info("🧠 **메모리 기능**\n- 이전 대화 기억\n- 개인 정보 저장")

with col3:
    st.info("🔧 **사용법**\n- 자유롭게 대화하세요\n- 개인 정보를 알려주세요")

# 예시 질문들
st.markdown("### 💡 시도해볼 수 있는 질문들:")
example_questions = [
    "내 이름은 김철수야. 나는 피자를 좋아해.",
    "내가 좋아하는 음식이 뭐였지?",
    "내 취미는 독서야. 특히 SF 소설을 좋아해.",
    "내 취미에 대해 기억하고 있어?",
    "나에 대해 무엇을 기억하고 있는지 정리해줘."
]

for i, question in enumerate(example_questions, 1):
    st.markdown(f"**{i}.** {question}")

# 디버그 정보 (개발자용)
if st.checkbox("🔍 디버그 정보 보기"):
    st.write("**세션 상태:**")
    st.write(f"- 메시지 수: {len(st.session_state.messages)}")
    st.write(f"- 에이전트 상태: {'✅ 초기화됨' if 'agent' in st.session_state else '❌ 미초기화'}")
    st.write(f"- 사용자 이름: {user_name}")
