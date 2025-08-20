import streamlit as st
from utils.course_utils import load_course_db, update_course_db, search_course, translate_reason

st.title("📚 Course Modality DB Manager")

# 엑셀 업로드
uploaded_file = st.file_uploader("강의 정보 엑셀 업로드", type=["xlsx"])
if uploaded_file:
    new_data = pd.read_excel(uploaded_file)
    update_course_db(new_data)
    st.success("강의 정보가 업데이트되었습니다.")

# 검색
db = load_course_db()
name = st.text_input("교원 이름 검색")
format = st.selectbox("Course Format", ["", "Online", "Offline", "Hybrid", "Blended(Over 70% online)", "Blended(Under 70% online)"])
semester = st.text_input("Year Semester")

filtered = search_course(name, format, semester, db)
if not filtered.empty:
    for _, row in filtered.iterrows():
        st.write(f"📘 {row['Course Title']} ({row['Course format']})")
        st.write(f"🧑‍🏫 Name: {row['Name']}")
        st.write(f"🗓️ Time: {row['Day']} {row['Time']}")
        st.write(f"📝 Reason (KR): {row['Reason for Applying']}")
        st.write(f"📝 Reason (EN): {translate_reason(row['Reason for Applying'])}")
        st.markdown("---")
