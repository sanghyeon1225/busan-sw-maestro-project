import streamlit as st
from pages import step1, step2, step3, home

st.set_page_config(
    page_title="냉장고 레시피",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 세션 상태 초기화
if "ingredients" not in st.session_state:
    st.session_state.ingredients = []          # [{name, checked}]
if "sauces" not in st.session_state:
    st.session_state.sauces = []
if "tools" not in st.session_state:
    st.session_state.tools = []
if "extra_ingredients" not in st.session_state:
    st.session_state.extra_ingredients = []
if "recipes" not in st.session_state:
    st.session_state.recipes = {}

PAGES = {
    "🏠 홈": home,
    "📷 Step 1 - 재료 입력": step1,
    "🧂 Step 2 - 재료 보강": step2,
    "🍳 Step 3 - 레시피 결과": step3,
}

with st.sidebar:
    st.title("🍳 냉장고 레시피")
    st.markdown("---")
    selection = st.radio("", list(PAGES.keys()), label_visibility="collapsed")

PAGES[selection].render()
