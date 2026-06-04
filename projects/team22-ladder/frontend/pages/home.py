import streamlit as st


def render():
    st.title("🍳 냉장고 레시피 추천")
    st.markdown("### 냉장고 속 재료로 만들 수 있는 레시피를 찾아드려요!")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        #### 📷 Step 1
        **재료 입력**

        사진을 찍거나 직접 입력해서
        냉장고 속 재료를 알려주세요.
        """)
    with col2:
        st.markdown("""
        #### 🧂 Step 2
        **재료 보강**

        소스, 조리도구, 추가 재료를
        선택해주세요.
        """)
    with col3:
        st.markdown("""
        #### 🍳 Step 3
        **레시피 추천**

        AI가 추천하는 레시피를
        확인해보세요!
        """)

    st.markdown("---")
    st.info("👈 왼쪽 사이드바에서 Step 1부터 시작하세요!")
