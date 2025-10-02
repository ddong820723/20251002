import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# 앱의 메인 제목 설정
st.title("📐 사각형 넓이로 이해하는 분배법칙 학습 앱")
st.markdown("버튼을 누르면 두 인접한 사각형이 무작위로 제시되고, 그 넓이를 분배법칙으로 구하는 과정을 시각적으로 보여줍니다.")

# ----------------------------------------------------
# 1. 시각화 함수 (Matplotlib으로 사각형 그리기)
# ----------------------------------------------------
def plot_rectangles(a, b, h):
    """높이 H, 밑변 A와 B인 두 사각형을 그립니다."""
    
    # Matplotlib 그림 영역 생성
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # 첫 번째 사각형 (노란색, 밑변 A, 높이 H)
    rect1 = plt.Rectangle((0, 0), a, h, facecolor='gold', edgecolor='black', linewidth=2)
    ax.add_patch(rect1)
    
    # 두 번째 사각형 (하늘색, 밑변 B, 높이 H)
    rect2 = plt.Rectangle((a, 0), b, h, facecolor='skyblue', edgecolor='black', linewidth=2)
    ax.add_patch(rect2)
    
    # 전체 사각형의 경계
    ax.plot([0, a + b, a + b, 0, 0], [h, h, 0, 0, h], color='red', linestyle='--')
    
    # 가로축(밑변) 길이 표시
    ax.text(a/2, -h*0.1, f'A ({a})', ha='center', fontsize=12, color='darkorange')
    ax.text(a + b/2, -h*0.1, f'B ({b})', ha='center', fontsize=12, color='darkblue')
    
    # 높이 표시
    ax.text(-0.1 * (a + b), h/2, f'H ({h})', va='center', fontsize=12)

    # 축 범위 설정
    ax.set_xlim(-0.2 * (a + b), a + b + 0.1 * (a + b))
    ax.set_ylim(-h * 0.2, h * 1.2)
    
    # 축 숨기기
    ax.axis('off')
    ax.set_aspect('equal', adjustable='box')
    
    return fig

# ----------------------------------------------------
# 2. 문제 생성 함수 (랜덤 정수/유리수 생성)
# ----------------------------------------------------
def generate_problem():
    # 높이(H)는 정수, 밑변(A, B)은 유리수(정수 포함)로 난이도 조절
    
    # 높이 (H): -10 ~ 10 사이의 0이 아닌 정수
    H = random.randint(-5, 5)
    while H == 0:
        H = random.randint(-5, 5)
        
    # 밑변 A와 B: 분수 형태를 표현하기 위해 0.5 단위의 유리수
    # 또는 간단하게 정수 -5~5 사이
    A = random.choice([x * 0.5 for x in range(-10, 11) if x != 0 and x * 0.5 != 0])
    B = random.choice([x * 0.5 for x in range(-10, 11) if x != 0 and x * 0.5 != 0])

    # 시각화를 위해 길이(절댓값) 사용
    visual_H = abs(H)
    visual_A = abs(A)
    visual_B = abs(B)

    # 분배법칙을 적용해야 할 식
    problem = f"{H} \\times ({A} + {B})"
    
    # 정답 계산: H * (A + B)
    answer = H * (A + B)
    
    # 분배법칙 적용 과정
    process = f"""
    1. **분배법칙 적용**:
       $${H} \\times {A} + {H} \\times {B}$$
    2. **각 항 계산**:
       $${H * A} + {H * B}$$
    3. **최종 합산**:
       $${answer}$$
    """
    
    return problem, process, answer, visual_H, visual_A, visual_B

# ----------------------------------------------------
# 3. Streamlit 세션 및 UI 구성
# ----------------------------------------------------

# 세션 상태 초기화 (문제 저장을 위해 필요)
if 'problem' not in st.session_state:
    st.session_state.problem, st.session_state.process, st.session_state.answer, st.session_state.visual_H, st.session_state.visual_A, st.session_state.visual_B = generate_problem()

# 새로운 문제 생성 버튼 (어느 칸을 클릭하면 -> 버튼 클릭으로 대체)
if st.button("✨ 새로운 문제 생성하기"):
    st.session_state.problem, st.session_state.process, st.session_state.answer, st.session_state.visual_H, st.session_state.visual_A, st.session_state.visual_B = generate_problem()

st.write("---")

# 1. 시각화 영역 (사각형 제시)
st.subheader("1. 사각형 제시")
st.pyplot(plot_rectangles(st.session_state.visual_A, st.session_state.visual_B, st.session_state.visual_H))
st.caption(f"제시된 사각형의 높이(H)는 {st.session_state.visual_H}, 밑변은 {st.session_state.visual_A}와 {st.session_state.visual_B}입니다.")

# 2. 문제 제시 영역 (분배법칙 식)
st.subheader("2. 분배법칙으로 넓이 구하기")
st.markdown("이 전체 넓이를 구하는 식은 다음과 같습니다. (높이와 밑변은 무작위 정수/유리수 값입니다.)")

# 분배법칙 식 (LaTeX으로 예쁘게 표시)
st.latex(st.session_state.problem)

st.write("---")

# 3. 풀이 및 과정 시각화 영역
with st.expander("✅ 풀이 과정 시각화 보기"):
    st.markdown("**1. 넓이 합산 공식**")
    st.latex(f"\\text{{전체 넓이}} = H \\times (A + B)")

    st.markdown("**2. 분배법칙 적용 공식**")
    st.latex(f"\\text{{전체 넓이}} = (H \\times A) + (H \\times B)")

    st.markdown("**3. 실제 값 대입 및 계산**")
    st.markdown(st.session_state.process, unsafe_allow_html=True) # HTML을 허용하여 줄바꿈 적용

    st.success(f"최종 넓이 (정답): **{st.session_state.answer}**")
