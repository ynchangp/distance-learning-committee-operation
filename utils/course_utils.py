import pandas as pd
from deep_translator import GoogleTranslator

COURSE_DB_PATH = 'data/course_modality_db.xlsx'

def load_course_db(path=COURSE_DB_PATH):
    """강의 DB 로드"""
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Name", "Year Semester", "Language", "Course Title", "Time Slot",
            "Day", "Time", "Frequency", "Course format", "Reason for Applying", "Modified"
        ])

def update_course_db(new_data, path=COURSE_DB_PATH):
    """강의 DB 업데이트 (병합 후 중복 제거)"""
    existing = load_course_db(path)
    combined = pd.concat([existing, new_data], ignore_index=True)
    combined.drop_duplicates(subset=["Name", "Course Title"], keep="last", inplace=True)
    combined.to_excel(path, index=False)

def search_course(name=None, format=None, semester=None, db=None):
    """강의 정보 검색"""
    if db is None:
        db = load_course_db()
    df = db.copy()

    if name:
        df = df[df["Name"].str.contains(name, case=False, na=False)]
    if format:
        df = df[df["Course format"].str.contains(format, case=False, na=False)]
    if semester:
        df = df[df["Year Semester"].str.contains(semester, case=False, na=False)]

    return df

def translate_reason(text):
    """Reason for Applying 번역"""
    if pd.isna(text) or str(text).strip().lower() == "none":
        return "None"
    try:
        return GoogleTranslator(source='ko', target='en').translate(text)
    except Exception:
        return "Translation Error"

def get_semester_filtered_data(semester, db=None):
    """특정 학기 데이터 필터링"""
    if db is None:
        db = load_course_db()
    return db[db["Year Semester"] == semester]

def match_english_names(course_df, faculty_df):
    """국문명 → 영문명 매칭"""
    name_map = faculty_df.set_index("Korean_name")["English_name"].to_dict()
    course_df["English_name"] = course_df["Name"].map(name_map).fillna("Unknown")
    return course_df
