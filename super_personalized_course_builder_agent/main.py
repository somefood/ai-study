import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI  # 또는 사용하고자 하는 LLM
from dotenv import load_dotenv

_ = load_dotenv()

# 상태 정의
class GraphState(TypedDict):
    user_profiles: List[str]
    user_interests: List[str]
    course_name: str
    course_approved: bool
    messages: List[str]


# LLM 초기화 (OpenAI API 키 필요)
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
)


def generate_course_name(state: GraphState) -> GraphState:
    """
    유저의 프로필과 관심사를 받아서 coursename을 생성하는 노드
    """
    user_profiles = state["user_profiles"]
    user_interests = state["user_interests"]

    # 프로필과 관심사를 문자열로 변환
    profiles_text = "\n".join([f"- {profile}" for profile in user_profiles])
    interests_text = "\n".join([f"- {interest}" for interest in user_interests])

    # 프롬프트 생성
    prompt = f"""
    사용자 프로필:
    {profiles_text}

    사용자 관심사:
    {interests_text}

    위 사용자의 프로필과 관심사를 종합적으로 분석하여 매력적이고 구체적인 코스명을 생성해주세요.
    사용자의 배경과 관심사에 모두 부합하는 코스명을 만들어주세요.
    코스명은 한국어로 작성하고, 학습자가 흥미를 느낄 수 있도록 만들어주세요.

    코스명만 답변해주세요.
    """

    # LLM 호출
    response = llm.invoke([HumanMessage(content=prompt)])
    course_name = response.content.strip()

    # 상태 업데이트
    state["course_name"] = course_name
    state["course_approved"] = False  # 초기값
    state["messages"].append(f"생성된 코스명: {course_name}")

    return state


def validate_course_name(state: GraphState) -> GraphState:
    """
    코스명이 적절한지 검증하는 노드
    """
    course_name = state["course_name"]

    # 검증 프롬프트
    prompt = f"""
    코스명: "{course_name}"

    위 코스명이 다음 기준을 만족하는지 평가해주세요:
    1. 명확하고 이해하기 쉬운가?
    2. 학습자의 흥미를 끌 수 있는가?
    3. 너무 길거나 짧지 않은가?
    4. 전문적이면서도 접근하기 쉬운가?

    "승인" 또는 "거부" 중 하나로만 답변해주세요.
    """

    # LLM 호출
    response = llm.invoke([HumanMessage(content=prompt)])
    validation_result = response.content.strip()

    # 검증 결과에 따라 상태 업데이트
    if "승인" in validation_result:
        state["course_approved"] = True
        state["messages"].append(f"코스명 검증 완료: 승인됨")
    else:
        state["course_approved"] = False
        state["messages"].append(f"코스명 검증 완료: 거부됨 - 재생성 필요")

    return state


def regenerate_course_name(state: GraphState) -> GraphState:
    """
    코스명을 재생성하는 노드
    """
    user_profiles = state["user_profiles"]
    user_interests = state["user_interests"]
    previous_course_name = state["course_name"]

    # 프로필과 관심사를 문자열로 변환
    profiles_text = "\n".join([f"- {profile}" for profile in user_profiles])
    interests_text = "\n".join([f"- {interest}" for interest in user_interests])

    # 재생성 프롬프트
    prompt = f"""
    사용자 프로필:
    {profiles_text}

    사용자 관심사:
    {interests_text}

    이전 코스명: {previous_course_name}

    이전 코스명이 부적절하다고 판단되어 새로운 코스명을 생성해야 합니다.
    사용자의 프로필과 관심사를 더 잘 반영하고, 더 매력적이고 명확한 코스명을 생성해주세요.

    코스명만 답변해주세요.
    """

    # LLM 호출
    response = llm.invoke([HumanMessage(content=prompt)])
    new_course_name = response.content.strip()

    # 상태 업데이트
    state["course_name"] = new_course_name
    state["course_approved"] = False  # 다시 검증 필요
    state["messages"].append(f"코스명 재생성: {new_course_name}")

    return state


def course_approval_router(state: GraphState) -> str:
    """
    코스명 승인 여부에 따라 다음 노드를 결정하는 조건부 라우터
    """
    if state["course_approved"]:
        return "approved"
    else:
        return "rejected"


def finalize_course(state: GraphState) -> GraphState:
    """
    최종 승인된 코스명을 처리하는 노드
    """
    state["messages"].append(f"최종 코스명 확정: {state['course_name']}")
    return state


# 그래프 구성
def create_course_name_graph():
    # StateGraph 생성
    workflow = StateGraph(GraphState)

    # 노드 추가
    workflow.add_node("generate_course_name", generate_course_name)
    workflow.add_node("validate_course_name", validate_course_name)
    workflow.add_node("regenerate_course_name", regenerate_course_name)
    workflow.add_node("finalize_course", finalize_course)

    # 시작점 설정
    workflow.set_entry_point("generate_course_name")

    # 엣지 연결
    workflow.add_edge("generate_course_name", "validate_course_name")

    # 조건부 엣지 추가
    workflow.add_conditional_edges(
        "validate_course_name",
        course_approval_router,
        {
            "approved": "finalize_course",
            "rejected": "regenerate_course_name"
        }
    )

    # 재생성 후 다시 검증으로 이동
    workflow.add_edge("regenerate_course_name", "validate_course_name")

    # 최종 승인 후 종료
    workflow.add_edge("finalize_course", END)

    # 그래프 컴파일
    app = workflow.compile()

    return app


# 실행 함수
def run_course_generator(user_data: dict):
    """
    코스명 생성기 실행
    """
    app = create_course_name_graph()

    # 초기 상태 설정
    initial_state = {
        "user_profiles": user_data["user_profiles"],
        "user_interests": user_data["user_interests"],
        "course_name": "",
        "course_approved": False,
        "messages": []
    }

    # 그래프 실행
    result = app.invoke(initial_state)

    return result


# 사용 예시
if __name__ == "__main__":
    # 사용자 데이터 입력
    user_data = {
        "user_profiles": [
            "User is a software engineer",
            "User wants to work abroad, specifically in the US",
            "User recently broke up with his girlfriend"
        ],
        "user_interests": [
            "Playing football",
            "Playing pickleball",
            "Riding a bike",
            "Hitting the gym",
            "Interested in AI technology"
        ]
    }

    # 코스명 생성 실행
    result = run_course_generator(user_data)

    print("=== 사용자 프로필 ===")
    for profile in result['user_profiles']:
        print(f"- {profile}")

    print("\n=== 사용자 관심사 ===")
    for interest in result['user_interests']:
        print(f"- {interest}")

    print(f"\n=== 결과 ===")
    print(f"생성된 코스명: {result['course_name']}")
    print(f"코스명 승인 여부: {result['course_approved']}")

    print("\n=== 메시지 히스토리 ===")
    for msg in result['messages']:
        print(f"- {msg}")
