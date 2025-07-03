from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    message: str
    step: int

def greet_node(state: State) -> State:
    return {
        "message": f"안녕하세요! 현재 단계: {state['step']}",
        "step": state["step"] + 1
    }

def process_node(state: State) -> State:
    return {
        "message": f"{state['message']} -> 처리 중...",
        "step": state["step"] + 1
    }

def end_node(state: State) -> State:
    return {
        "message": f"{state['message']} -> 완료!",
        "step": state["step"] + 1
    }

def build_graph():
    graph = StateGraph(State)
    
    graph.add_node("greet", greet_node)
    graph.add_node("process", process_node)
    graph.add_node("end", end_node)
    
    graph.set_entry_point("greet")
    graph.add_edge("greet", "process")
    graph.add_edge("process", "end")
    graph.add_edge("end", END)
    
    return graph.compile()

if __name__ == "__main__":
    app = build_graph()
    
    initial_state = {
        "message": "시작",
        "step": 0
    }
    
    print("LangGraph 초간단 예제 실행:")
    print("-" * 30)
    
    for output in app.stream(initial_state):
        for key, value in output.items():
            print(f"노드 '{key}': {value['message']}")
    
    print("-" * 30)
    print("완료!")