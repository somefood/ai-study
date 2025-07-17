import os
from typing import List

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from dotenv import load_dotenv

_ = load_dotenv()

class GraphState(TypedDict):
    user_interest: str
    course_name: str
    messages: List[str]


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
)


def generate_course_name(state: GraphState) -> GraphState:
    """
    유저의 관심사를 받아서 coursename을 생성하는 노드
    """
    user_interest = state["user_interest"]

    # 프롬프트 생성
    prompt = f"""
    사용자의 관심사: {user_interest}

    위 관심사를 바탕으로 매력적이고 구체적인 코스명을 생성해주세요.
    코스명은 한국어로 작성하고, 학습자가 흥미를 느낄 수 있도록 만들어주세요.

    코스명만 답변해주세요.
    """

    # LLM 호출
    response = llm.invoke([HumanMessage(content=prompt)])
    course_name = response.content.strip()

    # 상태 업데이트
    state["course_name"] = course_name
    state["messages"].append(f"생성된 코스명: {course_name}")

    return state


# 그래프 구성
def create_course_name_graph():
    # StateGraph 생성
    workflow = StateGraph(GraphState)

    # 노드 추가
    workflow.add_node("generate_course_name", generate_course_name)

    # 시작점 설정
    workflow.set_entry_point("generate_course_name")

    # 종료점 설정
    workflow.add_edge("generate_course_name", END)

    # 그래프 컴파일
    app = workflow.compile()

    return app


# 실행 함수
def run_course_generator(user_interest: str):
    """
    코스명 생성기 실행
    """
    app = create_course_name_graph()

    # 초기 상태 설정
    initial_state = {
        "user_interest": user_interest,
        "course_name": "",
        "messages": []
    }

    # 그래프 실행
    result = app.invoke(initial_state)

    return result

# 사용 예시
if __name__ == "__main__":
    # 사용자 관심사 입력
    user_interest = "영국 축구에 대해서 알고싶어"

    # 코스명 생성 실행
    result = run_course_generator(user_interest)

    print(f"사용자 관심사: {result['user_interest']}")
    print(f"생성된 코스명: {result['course_name']}")
    print("\n메시지 히스토리:")
    for msg in result['messages']:
        print(f"- {msg}")
