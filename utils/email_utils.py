import pandas as pd

FACULTY_DB_PATH = 'data/faculty_db.xlsx'

def load_faculty_db(path=FACULTY_DB_PATH):
    """교원 DB 로드"""
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Korean_name", "English_name", "Category", "Email"])

def update_faculty_db(new_data, path=FACULTY_DB_PATH):
    """교원 DB 업데이트 (병합 후 중복 제거)"""
    existing = load_faculty_db(path)
    combined = pd.concat([existing, new_data], ignore_index=True)
    combined.drop_duplicates(subset=["Korean_name", "English_name"], keep="last", inplace=True)
    combined.to_excel(path, index=False)

def find_email_by_name(name, db=None):
    """이름으로 이메일 검색 (국문 또는 영문)"""
    if db is None:
        db = load_faculty_db()
    result = db[(db["Korean_name"].str.lower() == name.lower()) | (db["English_name"].str.lower() == name.lower())]
    if not result.empty:
        return result.iloc[0]["Email"]
    return None

def get_english_name(korean_name, db=None):
    """국문명으로 영문명 검색"""
    if db is None:
        db = load_faculty_db()
    result = db[db["Korean_name"].str.lower() == korean_name.lower()]
    if not result.empty:
        return result.iloc[0]["English_name"]
    return "Unknown"
