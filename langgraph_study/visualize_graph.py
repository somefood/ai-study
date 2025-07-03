import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

def create_graph_visualization():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # 노드 위치 설정
    positions = {
        'START': (0, 0),
        'greet': (2, 0),
        'process': (4, 0),
        'end': (6, 0),
        'END': (8, 0)
    }
    
    # 노드 그리기
    node_colors = {
        'START': '#90EE90',    # 연한 초록
        'greet': '#87CEEB',    # 하늘색
        'process': '#DDA0DD',  # 자두색
        'end': '#F0E68C',      # 카키색
        'END': '#FFB6C1'       # 연한 분홍
    }
    
    # 노드 박스 그리기
    for node, (x, y) in positions.items():
        if node == 'START':
            label = '시작'
        elif node == 'greet':
            label = '인사\n(greet_node)'
        elif node == 'process':
            label = '처리\n(process_node)'
        elif node == 'end':
            label = '종료\n(end_node)'
        else:
            label = '끝'
            
        # 노드 박스
        box = FancyBboxPatch(
            (x-0.7, y-0.3), 1.4, 0.6,
            boxstyle="round,pad=0.1",
            facecolor=node_colors[node],
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(box)
        
        # 노드 텍스트
        ax.text(x, y, label, ha='center', va='center', 
                fontsize=10, fontweight='bold', fontfamily='Malgun Gothic')
    
    # 화살표 그리기
    arrow_props = dict(arrowstyle='->', lw=2, color='black')
    
    # START -> greet
    ax.annotate('', xy=(1.3, 0), xytext=(0.7, 0), arrowprops=arrow_props)
    
    # greet -> process
    ax.annotate('', xy=(3.3, 0), xytext=(2.7, 0), arrowprops=arrow_props)
    
    # process -> end
    ax.annotate('', xy=(5.3, 0), xytext=(4.7, 0), arrowprops=arrow_props)
    
    # end -> END
    ax.annotate('', xy=(7.3, 0), xytext=(6.7, 0), arrowprops=arrow_props)
    
    # 제목
    ax.text(4, 1.2, 'LangGraph 워크플로우', ha='center', va='center', 
            fontsize=16, fontweight='bold', fontfamily='Malgun Gothic')
    
    # 설명 텍스트
    description = """
    1. greet: 인사 메시지 생성
    2. process: 메시지 처리
    3. end: 완료 메시지 생성
    """
    ax.text(4, -1.5, description, ha='center', va='top', 
            fontsize=10, fontfamily='Malgun Gothic',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.7))
    
    # 축 설정
    ax.set_xlim(-1, 9)
    ax.set_ylim(-2.5, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('/Users/seokju/PycharmProjects/ai-study/langgraph_study/graph_visualization.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("그래프 시각화 이미지가 'graph_visualization.png'로 저장되었습니다!")

if __name__ == "__main__":
    create_graph_visualization()