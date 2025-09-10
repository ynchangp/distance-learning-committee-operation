import streamlit as st
import pandas as pd
import io
from utils.course_utils import (
    load_course_db,
    update_course_db,
    search_course,
    translate_reason
)
from utils.email_utils import load_faculty_db

st.set_page_config(page_title="Course Modality DB", layout="wide")
st.title("📚 Course Modality DB Manager")

# Load DBs
course_db = load_course_db()
faculty_db = load_faculty_db()

# --- Excel Upload ---
st.header("📤 엑셀로 강의 정보 업로드")
uploaded_file = st.file_uploader("강의 정보 엑셀 파일을 업로드하세요", type=["xlsx"])
if uploaded_file:
    new_data = pd.read_excel(uploaded_file)
    update_course_db(new_data)
    st.success("강의 정보가 성공적으로 업데이트되었습니다.")

st.divider()

# --- 개별 입력 ---
st.header("📝 개별 강의 정보 입력 및 수정")
with st.form("course_form"):
    name = st.text_input("Name")
    semester = st.text_input("Year Semester")
    language = st.selectbox("Language", ["en", "ko"])
    title = st.text_input("Course Title")
    slot = st.text_input("Time Slot")
    day = st.text_input("Day")
    time = st.text_input("Time")
    freq = st.text_input("Frequency")
    format = st.selectbox("Course format", [
        "Online", "Offline", "Hybrid",
        "Blended(Over 70% online)", "Blended(Under 70% online)"
    ])
    reason = st.text_area("Reason for Applying")
    modified = st.text_input("Modified (YYYY-MM-DD HH:MM:SS)")
    submitted = st.form_submit_button("저장")
    if submitted:
        new_row = pd.DataFrame([{
            "Name": name,
            "Year Semester": semester,
            "Language": language,
            "Course Title": title,
            "Time Slot": slot,
            "Day": day,
            "Time": time,
            "Frequency": freq,
            "Course format": format,
            "Reason for Applying": reason if reason else "None",
            "Modified": modified
        }])
        update_course_db(new_row)
        st.success("강의 정보가 저장되었습니다.")

st.divider()

# --- 검색 기능 ---
st.header("🔍 강의 정보 검색")
col1, col2, col3 = st.columns(3)
with col1:
    search_name = st.text_input("검색할 교원 이름")
with col2:
    search_format = st.selectbox("검색할 Course Format", ["", "Online", "Offline", "Hybrid", "Blended(Over 70% online)", "Blended(Under 70% online)"])
with col3:
    search_semester = st.text_input("검색할 Year Semester")

filtered = search_course(search_name, search_format, search_semester, course_db)

if not filtered.empty:
    st.subheader("📋 검색 결과")
    for _, row in filtered.iterrows():
        st.markdown(f"### {row['Course Title']} ({row['Course format']})")
        st.write(f"👤 Name: {row['Name']}")
        st.write(f"🗓️ Day & Time: {row['Day']} {row['Time']}")
        st.write(f"🧾 Reason (KR): {row['Reason for Applying']}")
        st.write(f"🌐 Reason (EN): {translate_reason(row['Reason for Applying'])}")
        st.write(f"🕒 Modified: {row['Modified']}")
        st.markdown("---")
else:
    st.info("검색 결과가 없습니다.")

st.divider()

# --- 전체 다운로드 ---
st.header("📥 전체 강의 정보 다운로드")
if st.button("전체 다운로드 (국문명 + 영문명 포함)"):
    df = course_db.copy()
    name_map = faculty_db.set_index("Korean_name")["English_name"].to_dict()
    df["English_name"] = df["Name"].map(name_map).fillna("Unknown")
    output = io.BytesIO()
    df.to_excel(output, index=False)
    st.download_button(
        label="엑셀 다운로드",
        data=output.getvalue(),
        file_name="course_modality_full.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.divider()

# --- 학기별 다운로드 ---
st.header("📥 학기별 강의 정보 다운로드")
semester_filter = st.text_input("다운로드할 Year Semester")
if st.button("학기별 다운로드"):
    df = course_db[course_db["Year Semester"] == semester_filter]
    if not df.empty:
        name_map = faculty_db.set_index("Korean_name")["English_name"].to_dict()
        df["English_name"] = df["Name"].map(name_map).fillna("Unknown")
        output = io.BytesIO()
        df.to_excel(output, index=False)
        st.download_button(
            label="엑셀 다운로드",
            data=output.getvalue(),
            file_name=f"course_modality_{semester_filter}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("해당 학기에 대한 정보가 없습니다.")

