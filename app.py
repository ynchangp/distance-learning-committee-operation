import streamlit as st

st.set_page_config(page_title="Distance Learning Committee", layout="wide")

st.title("Distance Learning Committee Operation")
st.markdown("📧 Faculty Email Finder와 📚 Course Modality DB를 관리하는 통합 플랫폼입니다.")

# 사이드바 메뉴
menu = st.sidebar.selectbox(
    "기능을 선택하세요",
    ["홈", "Faculty Email Finder", "Course Modality DB"]
)

# 기능별 화면 분기
if menu == "홈":
    st.markdown("""
    ### 👋 환영합니다!
    이 플랫폼은 Distance Learning Committee 운영을 위한 통합 도구입니다.

    **왼쪽 사이드바**에서 기능을 선택해 주세요:
    - 📧 Faculty Email Finder: 교원 이메일 자동 매칭
    - 📚 Course Modality DB: 강의 정보 관리 및 다운로드
    """)

elif menu == "Faculty Email Finder":
    st.markdown("### 📧 Faculty Email Finder")
    st.markdown("이름 기반 이메일 자동 매칭 기능을 여기에 구현하세요.")

elif menu == "Course Modality DB":
    st.markdown("### 📚 Course Modality DB")
    st.markdown("강의 정보 업로드 및 필터링 기능을 여기에 구현하세요.")


