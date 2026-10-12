import streamlit as st

st.set_page_config(page_title="학생 성적 데이터 소개", page_icon="🎓", layout="wide")

# 생성형 AI(Codex)가 실제 StudentsPerformance.csv를 확인하여 작성한 설명.
# 메인 페이지에는 데이터 설명만 표시합니다.
st.title("🎓 StudentsPerformance 데이터 소개")
st.markdown("""
**StudentsPerformance**는 학생의 배경 정보와 수학·읽기·쓰기 시험 점수를
함께 기록한 데이터입니다. 제공된 CSV에는 **학생 1,000명의 관측값과 8개 변수**가
있으며, 결측값은 없습니다.

배경 변수는 성별(`gender`), 인종·민족 범주(`race/ethnicity`),
부모의 교육 수준(`parental level of education`), 급식 유형(`lunch`),
시험 준비 과정 이수 여부(`test preparation course`)입니다.
성적 변수는 **수학(`math score`), 읽기(`reading score`), 쓰기(`writing score`)**이며,
점수는 0~100 범위입니다.

제공된 데이터의 과목별 평균은 수학 **66.09점**, 읽기 **69.17점**, 쓰기 **68.05점**입니다.
평균·중앙값·표준편차를 통해 성적의 중심과 흩어짐을 살펴보고,
점수 분포, 과목 간 상관관계, 배경 범주별 성적 차이를 탐색할 수 있습니다.
이러한 차이와 상관관계만으로 배경 특성이 성적의 원인이라고 해석할 수는 없습니다.
""")
st.caption("생성형 AI로 작성한 설명 · 제공된 StudentsPerformance.csv 기준")
