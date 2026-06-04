import streamlit as st


# 목업: 실제 구현 시 AI agent 호출로 대체
MOCK_INGREDIENTS_FROM_IMAGE = ["김치", "두부", "콩나물", "돼지고기", "달걀", "대파"]


def render():
    st.title("📷 Step 1 — 재료 입력")
    st.markdown("냉장고 속 재료를 알려주세요.")
    st.markdown("---")

    tab_image, tab_text = st.tabs(["📸 사진 업로드", "✏️ 직접 입력"])

    with tab_image:
        uploaded_files = st.file_uploader(
            "냉장고 사진을 업로드하세요 (여러 장 가능)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            cols = st.columns(min(len(uploaded_files), 4))
            for i, f in enumerate(uploaded_files):
                cols[i % 4].image(f, use_container_width=True)

            if st.button("🔍 재료 분석하기", key="analyze_btn", type="primary"):
                with st.spinner("재료를 분석하는 중..."):
                    # TODO: AI agent 호출
                    _load_ingredients(MOCK_INGREDIENTS_FROM_IMAGE)
                st.success("분석 완료!")
                st.rerun()

    with tab_text:
        st.markdown("재료를 한 줄에 하나씩 입력하세요.")
        text_input = st.text_area(
            "재료 목록",
            placeholder="예)\n김치\n두부\n돼지고기",
            height=150,
            label_visibility="collapsed",
        )
        if st.button("➕ 재료 추가", key="text_add_btn", type="primary"):
            if text_input.strip():
                items = [i.strip() for i in text_input.strip().splitlines() if i.strip()]
                _load_ingredients(items)
                st.success(f"{len(items)}개 재료가 추가됐어요!")
                st.rerun()

    # 재료 목록
    if st.session_state.ingredients:
        st.markdown("---")
        st.markdown("### 🥬 재료 목록")
        st.caption("우선적으로 사용하고 싶은 재료를 체크하세요. 체크할수록 레시피 추천 우선순위가 높아져요!")

        col_reset, col_check_all, _ = st.columns([1, 1, 5])
        with col_reset:
            if st.button("🗑️ 초기화"):
                st.session_state.ingredients = []
                st.rerun()
        with col_check_all:
            if st.button("✅ 전체 선택"):
                for item in st.session_state.ingredients:
                    item["checked"] = True
                st.rerun()

        st.markdown("")

        checked = [i for i in st.session_state.ingredients if i["checked"]]
        unchecked = [i for i in st.session_state.ingredients if not i["checked"]]
        ordered = checked + unchecked

        for item in ordered:
            col_chk, col_name, col_del = st.columns([0.5, 6, 0.8])
            new_val = col_chk.checkbox(
                "", value=item["checked"], key=f"chk_{item['name']}"
            )
            if new_val != item["checked"]:
                item["checked"] = new_val
                st.rerun()
            label = f"**{item['name']}**" if item["checked"] else item["name"]
            col_name.markdown(label)
            if col_del.button("✕", key=f"del_{item['name']}"):
                st.session_state.ingredients = [
                    i for i in st.session_state.ingredients if i["name"] != item["name"]
                ]
                st.rerun()

        st.markdown("---")
        priority_names = [i["name"] for i in st.session_state.ingredients if i["checked"]]
        if priority_names:
            st.markdown(f"⭐ **우선 재료**: {', '.join(priority_names)}")

        st.markdown("")
        if st.button("다음 단계로 →", type="primary", use_container_width=True):
            st.session_state["nav"] = "🧂 Step 2 - 재료 보강"
            st.info("👈 사이드바에서 Step 2로 이동하세요!")
    else:
        st.markdown("---")
        st.warning("아직 재료가 없어요. 위에서 사진을 업로드하거나 직접 입력해주세요!")


def _load_ingredients(names: list[str]):
    existing = {i["name"] for i in st.session_state.ingredients}
    for name in names:
        if name not in existing:
            st.session_state.ingredients.append({"name": name, "checked": False})
