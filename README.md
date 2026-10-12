# StudentsPerformance 멀티 페이지 시각화 앱

Streamlit과 Plotly로 만든 학생 성적 분석 실습 앱입니다.

- `streamlit_app.py`: 생성형 AI(Codex)가 실제 CSV를 확인해 작성한 간략한 데이터 설명만 표시합니다. 실행 시 AI API 키는 필요하지 않습니다.
- `pages/1_📊_성적_시각화.py`: CSV 업로드, 과목·배경 필터, 기술통계표, 히스토그램, 상자그림, 집단별 평균·학생 수, 산점도, 상관계수와 통계 CSV 다운로드를 제공합니다.
- `student_data.py`: 인코딩 처리, 필수 열 및 점수 검증, 통계 계산을 담당합니다.

## 실행

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

사이드바에서 **성적 시각화**를 선택하고 `StudentsPerformance.csv`를 업로드하세요.
제공된 CSV 다운로드와 예제 데이터 사용도 가능합니다. 업로드 파일이 있으면 예제보다 우선합니다.
UTF-8 및 CP949/EUC-KR 인코딩을 지원합니다.

필수 열은 `gender`, `race/ethnicity`, `parental level of education`, `lunch`,
`test preparation course`, `math score`, `reading score`, `writing score`입니다.
점수는 0~100의 숫자여야 하며 결측값은 통계 계산에서 제외합니다.
기술통계에는 유효 개수, 평균, 표본 표준편차, 최솟값, 사분위수, 중앙값, 최댓값, 결측값 수가 포함됩니다.

## 공유 및 배포

1. 이 프로젝트를 본인의 GitHub 저장소에 올립니다. `pages/`, `student_data.py`, `requirements.txt`, `StudentsPerformance.csv`도 포함하세요.
2. [Streamlit Community Cloud](https://share.streamlit.io/)에서 저장소와 브랜치를 선택합니다.
3. 메인 파일 경로를 `streamlit_app.py`로 지정하여 배포합니다.
4. 배포 후 생성되는 앱 URL을 공유합니다.

현재 프로젝트에는 실제 배포 URL이 없습니다. 기존 GDP 템플릿의 링크는 제거했습니다.

구현 참고: [Streamlit 멀티 페이지 공식 문서](https://docs.streamlit.io/develop/concepts/multipage-apps/pages-directory),
[Plotly 차트 표시](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart).
