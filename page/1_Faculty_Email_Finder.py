import streamlit as st
import pandas as pd
from utils.email_utils import load_faculty_db, update_faculty_db, find_email_by_name

st.title("📧 Faculty Email Finder")

# 엑셀 업로드
st.header("📤 교원 정보 엑셀 업로드")
uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])
if uploaded_file:
    new_data = pd.read_excel(uploaded_file)
    update_faculty_db(new_data)
    st.success("교원 정보가 업데이트되었습니다.")

# 개별 입력
st.header("📝 개별 교원 정보 입력")
with st.form("faculty_form"):
    kor_name = st.text_input("Korean Name")
    eng_name = st.text_input("English Name")
    category = st.text_input("Category")
    email = st.text_input("Email")
    submitted = st.form_submit_button("추가/수정")
    if submitted:
        new_row = pd.DataFrame([{
            "Korean_name": kor_name,
            "English_name": eng_name,
            "Category": category,
            "Email": email
        }])
        update_faculty_db(new_row)
        st.success("교원 정보가 저장되었습니다.")

# 이메일 검색
st.header("🔍 이메일 검색")
search_name = st.text_input("이름으로 이메일 검색 (국문 또는 영문)")
if search_name:
    db = load_faculty_db()
    result = find_email_by_name(search_name, db)
    if result:
        st.success(f"이메일: {result}")
    else:
        st.warning("해당 이름의 이메일을 찾을 수 없습니다.")


