"""학생 성적 CSV 읽기, 검증 및 기술통계 계산."""
from io import StringIO

import pandas as pd

SCORES = ["math score", "reading score", "writing score"]
CATEGORIES = [
    "gender", "race/ethnicity", "parental level of education",
    "lunch", "test preparation course",
]
LABELS = {
    "math score": "수학", "reading score": "읽기", "writing score": "쓰기",
    "gender": "성별", "race/ethnicity": "인종·민족 범주",
    "parental level of education": "부모 교육 수준", "lunch": "급식 유형",
    "test preparation course": "시험 준비 과정",
}


def load_students(content: bytes, encoding: str = "자동") -> pd.DataFrame:
    if not content.strip():
        raise ValueError("빈 파일입니다. 데이터가 있는 CSV를 업로드해 주세요.")
    encodings = ["utf-8-sig", "cp949", "euc-kr"] if encoding == "자동" else [encoding]
    text = None
    for candidate in encodings:
        try:
            text = content.decode(candidate)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise ValueError("인코딩을 읽을 수 없습니다. UTF-8 또는 CP949로 저장해 주세요.")
    try:
        frame = pd.read_csv(StringIO(text))
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError("CSV 형식을 확인해 주세요. 쉼표로 구분된 파일이어야 합니다.") from exc
    frame.columns = frame.columns.str.strip()
    if frame.columns.duplicated().any():
        raise ValueError("같은 이름의 열이 중복되어 있습니다. 열 이름을 확인해 주세요.")
    missing = [col for col in CATEGORIES + SCORES if col not in frame.columns]
    if missing:
        raise ValueError("필수 열이 없습니다: " + ", ".join(missing))
    if frame.empty:
        raise ValueError("열 제목만 있고 학생 데이터가 없습니다.")
    for col in SCORES:
        original = frame[col]
        numeric = pd.to_numeric(original, errors="coerce")
        invalid = original.notna() & numeric.isna()
        if invalid.any():
            raise ValueError(f"{col}에 숫자가 아닌 값이 {int(invalid.sum())}개 있습니다.")
        if (numeric.notna() & ~numeric.between(0, 100)).any():
            raise ValueError(f"{col} 점수는 0~100 범위여야 합니다.")
        frame[col] = numeric.astype(float)
    for col in CATEGORIES:
        frame[col] = frame[col].astype("string").str.strip().replace("", pd.NA)
    return frame


def descriptive_stats(frame: pd.DataFrame, scores: list[str]) -> pd.DataFrame:
    result = frame[scores].describe().T.rename(columns={
        "count": "유효 개수", "mean": "평균", "std": "표준편차",
        "min": "최솟값", "25%": "1사분위수", "50%": "중앙값",
        "75%": "3사분위수", "max": "최댓값",
    })
    result["결측값 수"] = frame[scores].isna().sum()
    result.index = [LABELS[col] for col in result.index]
    return result
