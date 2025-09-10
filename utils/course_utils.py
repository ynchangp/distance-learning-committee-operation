import pandas as pd
from deep_translator import GoogleTranslator

def load_course_db(path='data/course_modality_db.xlsx'):
    return pd.read_excel(path)

def update_course_db(new_data, path='data/course_modality_db.xlsx'):
    existing = load_course_db(path)
    combined = pd.concat([existing, new_data]).drop_duplicates(subset=['Name', 'Course Title'], keep='last')
    combined.to_excel(path, index=False)

def search_course(name=None, format=None, semester=None, db=None):
    df = db.copy()
    if name:
        df = df[df['Name'].str.contains(name, case=False)]
    if format:
        df = df[df['Course format'].str.contains(format, case=False)]
    if semester:
        df = df[df['Year Semester'].str.contains(semester, case=False)]
    return df

def translate_reason(text):
    if pd.isna(text) or text.strip().lower() == 'none':
        return 'None'
    return GoogleTranslator(source='ko', target='en').translate(text)
