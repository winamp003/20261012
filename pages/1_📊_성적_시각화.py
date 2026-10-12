import plotly.express as px
import streamlit as st

from student_data import CATEGORIES, LABELS, SCORES, descriptive_stats, load_students

st.set_page_config(page_title="학생 성적 시각화", page_icon="📊", layout="wide")
st.title("📊 학생 성적 시각화")
st.write("StudentsPerformance CSV를 업로드하여 과목별 성적과 학생 배경을 탐색하세요.")
uploaded = st.file_uploader("StudentsPerformance.csv 업로드", type=["csv"])
with st.expander("CSV 인코딩 설정"):
    encoding = st.selectbox("문자 인코딩", ["자동", "utf-8-sig", "cp949", "euc-kr"])
if uploaded is None:
    st.info("분석을 시작하려면 CSV 파일을 업로드해 주세요.")
    st.stop()
try:
    data = load_students(uploaded.getvalue(), encoding)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
st.caption(f"분석 파일: {uploaded.name}")

st.sidebar.header("분석 조건")
selected = st.sidebar.multiselect("분석 과목", SCORES, default=SCORES, format_func=lambda col: LABELS[col])
filtered = data.copy()
with st.sidebar.expander("학생 배경 필터"):
    for category in CATEGORIES:
        # 실제 범주와 결측값을 구분하도록 결측값에는 None을 사용합니다.
        options = sorted(data[category].dropna().unique().tolist())
        if data[category].isna().any():
            options.append(None)
        chosen = st.multiselect(LABELS[category], options, default=options,
                                format_func=lambda value: "(결측값)" if value is None else value)
        mask = filtered[category].isin([value for value in chosen if value is not None])
        if None in chosen:
            mask = mask | filtered[category].isna()
        filtered = filtered[mask]

count, total, missing = st.columns(3)
count.metric("분석 학생 수", f"{len(filtered):,}명")
total.metric("전체 학생 수", f"{len(data):,}명")
missing.metric("성적 결측값 수", f"{int(filtered[SCORES].isna().sum().sum()):,}개")
st.caption("필터를 적용한 전체 학생으로 통계와 차트를 계산합니다. 결측 성적은 해당 계산에서 제외합니다.")
with st.expander("데이터 미리보기"):
    st.dataframe(filtered.head(100), width="stretch")
    st.caption("최대 100행 표시")
if filtered.empty:
    st.warning("조건에 맞는 학생이 없습니다. 배경 필터를 변경해 주세요.")
    st.stop()
if not selected:
    st.info("분석할 과목을 하나 이상 선택해 주세요.")
    st.stop()

st.subheader("과목별 기술통계")
stats = descriptive_stats(filtered, selected)
st.dataframe(stats.round(2), width="stretch")
st.caption("표준편차는 표본 기준(ddof=1)입니다. 유효 점수가 부족하면 일부 통계가 빈칸으로 표시됩니다.")
st.download_button("기술통계 CSV 다운로드", stats.to_csv().encode("utf-8-sig"), "student_statistics.csv", "text/csv")
if not filtered[selected].notna().any().any():
    st.warning("선택한 과목에 유효한 점수가 없습니다.")
    st.stop()

long = filtered.melt(id_vars=CATEGORIES, value_vars=selected, var_name="과목", value_name="점수")
long["과목"] = long["과목"].map(LABELS)
valid = long.dropna(subset=["점수"])
distribution, groups, relationship = st.tabs(["점수 분포", "집단별 비교", "과목 간 관계"])
with distribution:
    bins = st.slider("히스토그램 구간 수", 5, 50, 20)
    st.plotly_chart(px.histogram(valid, x="점수", color="과목", nbins=bins,
        barmode="overlay", opacity=0.65, title="과목별 점수 분포", range_x=[0, 100]), width="stretch")
    st.plotly_chart(px.box(valid, x="과목", y="점수", color="과목",
        title="중앙값·사분위수와 이상값", range_y=[0, 100]), width="stretch")
with groups:
    group = st.selectbox("비교할 배경 변수", CATEGORIES, format_func=lambda col: LABELS[col])
    grouped = valid.dropna(subset=[group])
    if grouped.empty:
        st.info("배경 변수와 점수가 모두 있는 학생이 없습니다.")
    else:
        summary = grouped.groupby([group, "과목"], observed=True)["점수"].agg(["mean", "count"]).reset_index()
        summary = summary.rename(columns={group: "집단", "mean": "평균 점수", "count": "유효 학생 수"})
        st.plotly_chart(px.bar(summary, x="집단", y="평균 점수", color="과목", barmode="group",
            hover_data=["유효 학생 수"], range_y=[0, 100], title=f"{LABELS[group]}별 평균 성적"), width="stretch")
        st.dataframe(summary, width="stretch", hide_index=True)
        st.plotly_chart(px.box(grouped, x=group, y="점수", color="과목",
            labels={group: LABELS[group]}, range_y=[0, 100], title="집단별 성적 분포"), width="stretch")
        counts = filtered[group].dropna().value_counts().rename_axis("집단").reset_index(name="학생 수")
        st.plotly_chart(px.bar(counts, x="집단", y="학생 수", title="집단별 학생 수"), width="stretch")
        st.caption("배경 변수의 결측값은 집단 비교에서 제외합니다. 집단 크기와 분포를 함께 확인하세요.")
with relationship:
    if len(selected) < 2:
        st.info("과목을 2개 이상 선택하면 산점도와 상관계수가 표시됩니다.")
    else:
        x = st.selectbox("X축 과목", selected, index=0, format_func=lambda col: LABELS[col])
        remaining = [col for col in selected if col != x]
        y = st.selectbox("Y축 과목", remaining, format_func=lambda col: LABELS[col])
        pairs = filtered.dropna(subset=[x, y])
        if pairs.empty:
            st.info("두 과목의 점수가 모두 있는 학생이 없습니다.")
        else:
            st.plotly_chart(px.scatter(pairs, x=x, y=y, opacity=0.6,
                labels=LABELS, range_x=[0, 100], range_y=[0, 100],
                title=f"{LABELS[x]}과 {LABELS[y]} 점수 관계"), width="stretch")
        corr = filtered[selected].corr(min_periods=2).rename(index=LABELS, columns=LABELS)
        if corr.notna().any().any():
            st.plotly_chart(px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1,
                color_continuous_scale="RdBu_r", title="피어슨 상관계수"), width="stretch")
        else:
            st.info("상관계수를 계산할 관측값이나 점수 변동이 부족합니다.")
        st.caption("각 과목 쌍의 유효 점수로 계산합니다. 상수 또는 관측값 부족은 빈칸이며, 상관관계는 인과관계를 뜻하지 않습니다.")
