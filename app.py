import streamlit as st
import pandas as pd

# 내부 DB 로드
db = pd.read_excel("final_professor_list_250813.xlsx")

st.title("📧 Faculty Email Finder")

tab1, tab2 = st.tabs(["엑셀 자동 매칭", "단일 검색"])

with tab1:
    uploaded_file = st.file_uploader("교원 이름만 있는 엑셀 업로드", type=["xlsx"])
    if uploaded_file:
        input_df = pd.read_excel(uploaded_file)
        input_df["이메일"] = input_df["이름"].map(
            lambda name: db.loc[(db["Korean_name"] == name) | (db["English_name"] == name), "Email"].values[0]
            if not db.loc[(db["Korean_name"] == name) | (db["English_name"] == name)].empty else "찾을 수 없음"
        )
        st.write(input_df)
        st.download_button("📥 결과 엑셀 다운로드", input_df.to_excel(index=False), file_name="matched_emails.xlsx")

with tab2:
    name = st.text_input("교원 이름 입력 (국문 또는 영문)")
    if name:
        result = db.loc[(db["Korean_name"] == name) | (db["English_name"] == name)]
        if not result.empty:
            st.success(f"이메일: {result['Email'].values[0]}")
        else:
            st.error("해당 교원을 찾을 수 없습니다.")

