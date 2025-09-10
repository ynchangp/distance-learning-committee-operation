import pandas as pd

def load_faculty_db(path='data/faculty_db.xlsx'):
    return pd.read_excel(path)

def update_faculty_db(new_data, path='data/faculty_db.xlsx'):
    existing = load_faculty_db(path)
    combined = pd.concat([existing, new_data]).drop_duplicates(subset=['Korean_name', 'English_name'], keep='last')
    combined.to_excel(path, index=False)

def find_email_by_name(name, db):
    result = db[(db['Korean_name'] == name) | (db['English_name'] == name)]
    return result['Email'].values[0] if not result.empty else None
