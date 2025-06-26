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

st.title("🧠 퀴즈 맞추기 메모리 챗봇")
st.markdown("LangMem을 사용해서 질문을 기억하며 퀴즈를 진행하는 챗봇입니다!")

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
        manage_memory_tool = create_manage_memory_tool(namespace=("quiz_memory",))
        search_memory_tool = create_search_memory_tool(namespace=("quiz_memory",))
        memory_tools = [manage_memory_tool, search_memory_tool]

        system_prompt = """당신은 LangMem 메모리 기능을 사용하는 퀴즈 맞추기 AI 에이전트입니다.

                        당신은 다음 두 가지 메모리 도구를 사용할 수 있습니다:
                        
                        - `manage_memory`: 당신이 한 **질문**과 사용자의 **답변**을 저장하거나 수정, 삭제할 때 사용합니다.
                        - `search_memory`: 이전에 저장한 질문과 답변을 검색하여 유사하거나 중복되지 않도록 할 때 사용합니다.
                        
                        🎯 목표:
                        - 사용자가 "시작"이라고 말하면 퀴즈를 시작합니다.
                        - 사용자가 마음속에 생각한 답을 맞히기 위해, **하나씩 질문을 던지며 좁혀나갑니다.**
                        - 사용자가 "정답!" 또는 "맞았어!"라고 말할 때까지 질문을 이어갑니다.
                        - 각 질문과 사용자의 답변을 `manage_memory`를 사용하여 저장해야 합니다.
                        - 새 질문을 하기 전에 반드시 `search_memory`로 이전 질문과 답변을 확인하세요.
                        
                        💡 대화 규칙:
                        - 질문은 짧고 명확하게 하세요. (예: "그건 동물인가요?", "전자제품인가요?")
                        - 사용자의 답변 (네/아니오) 바탕으로 다음 질문을 점점 더 구체적으로 만들어야 합니다.
                        - 질문은 한 번에 하나씩만 하세요.
                        - 질문을 반복하지 않도록 이전에 한 질문은 항상 메모리에서 확인하세요.
                        - 사용자가 "정답이야", "맞췄어", "정답!" 등의 표현을 하면 퀴즈를 종료하고 축하해주세요.
                        
                        📝 메모리 저장 형식:
                        질문: "그건 동물인가요?" / 답변: "네" 또는 "아니오"
                        이런 식으로 질문과 답변을 쌍으로 저장하세요.
                        
                        당신은 친근하고 호기심 많은 퀴즈 호스트처럼 행동해야 합니다. 대화를 즐겁게 이끌어가세요!"""

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
            "content": f"안녕하세요 {user_name}님! 🎯 퀴즈 맞추기 게임을 해보세요!\n\n마음속으로 무언가를 생각하시고 **'시작'**이라고 입력해주세요. 제가 질문으로 맞춰보겠습니다! 🤖"
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
                        "thread_id": f"quiz_{user_name}"
                    }
                }

                # 전체 대화 히스토리를 포함해서 에이전트에 전달
                conversation_messages = []

                # 최근 대화 히스토리 포함 (최대 10개 메시지)
                recent_messages = st.session_state.messages[-10:]
                for msg in recent_messages:
                    conversation_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

                # 현재 사용자 입력 추가
                conversation_messages.append({
                    "role": "user",
                    "content": user_input
                })

                # 에이전트 호출 - 전체 대화 히스토리 포함
                response = st.session_state.agent.invoke(
                    {"messages": conversation_messages},
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
    st.info("🎯 **퀴즈 게임**\n- '시작'으로 게임 시작\n- 네/아니오로 답변")

with col2:
    st.info("🧠 **메모리 기능**\n- 질문과 답변 기억\n- 중복 질문 방지")

with col3:
    st.info("🔧 **사용법**\n1. 무언가를 생각하세요\n2. '시작' 입력\n3. 질문에 답하세요")

# 예시 대화
st.markdown("### 💡 게임 진행 예시:")
example_flow = [
    "👤 **사용자**: 시작",
    "🤖 **챗봇**: 그것은 살아있는 것인가요?",
    "👤 **사용자**: 아니요",
    "🤖 **챗봇**: 그것은 전자제품인가요?",
    "👤 **사용자**: 네",
    "🤖 **챗봇**: 그것은 스마트폰인가요?"
]

for step in example_flow:
    st.markdown(step)

# 디버그 정보 (개발자용)
if st.checkbox("🔍 디버그 정보 보기"):
    st.write("**세션 상태:**")
    st.write(f"- 메시지 수: {len(st.session_state.messages)}")
    st.write(f"- 에이전트 상태: {'✅ 초기화됨' if 'agent' in st.session_state else '❌ 미초기화'}")
    st.write(f"- 사용자 이름: {user_name}")

    if st.checkbox("📜 전체 대화 히스토리 보기"):
        for i, msg in enumerate(st.session_state.messages):
            st.write(f"{i+1}. **{msg['role']}**: {msg['content'][:100]}...")
