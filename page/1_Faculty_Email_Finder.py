import streamlit as st
from utils.email_utils import load_faculty_db, update_faculty_db, find_email_by_name

st.title("📧 Faculty Email Finder")

# 엑셀 업로드
uploaded_file = st.file_uploader("교원 정보 엑셀 업로드", type=["xlsx"])
if uploaded_file:
    new_data = pd.read_excel(uploaded_file)
    update_faculty_db(new_data)
    st.success("교원 정보가 업데이트되었습니다.")

# 개별 입력
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

