import streamlit as st

st.set_page_config(page_title="학생 성적 데이터 소개", page_icon="🎓", layout="wide")

st.title("🎓 StudentsPerformance 데이터 소개")
st.markdown("""
**StudentsPerformance**는 학생의 배경 정보와 수학·읽기·쓰기 시험 점수를
함께 기록하는 데이터 형식입니다. CSV를 업로드하면 **8개 변수**를 바탕으로
학생별 성적과 배경 정보를 확인할 수 있습니다.

배경 변수는 성별(`gender`), 인종·민족 범주(`race/ethnicity`),
부모의 교육 수준(`parental level of education`), 급식 유형(`lunch`),
시험 준비 과정 이수 여부(`test preparation course`)입니다.
성적 변수는 **수학(`math score`), 읽기(`reading score`), 쓰기(`writing score`)**이며,
점수는 0~100 범위입니다.

평균·중앙값·표준편차를 통해 성적의 중심과 흩어짐을 살펴보고,
점수 분포, 과목 간 상관관계, 배경 범주별 성적 차이를 탐색할 수 있습니다.
이러한 차이와 상관관계만으로 배경 특성이 성적의 원인이라고 해석할 수는 없습니다.
""")
st.info("성적 시각화 페이지에서 분석할 CSV 파일을 업로드해 주세요.")
