import streamlit as st

DIFFICULTY_LABEL = {1: "매우 쉬움", 2: "쉬움", 3: "보통", 4: "어려움", 5: "매우 어려움"}


def render():
    st.title("🍳 레시피 추천")
    st.markdown("<hr style='margin:4px 0 20px;border-color:#e5e7eb'>", unsafe_allow_html=True)

    recipes = st.session_state.get("recipes", {})

    if not recipes:
        st.warning("아직 레시피가 없어요. 재료 보강 단계에서 레시피를 생성해주세요.")
        return

    owned = {i["name"] for i in st.session_state.get("ingredients", [])}
    owned |= set(st.session_state.get("sauces", []))
    owned |= set(st.session_state.get("extra_ingredients", []))

    st.markdown("## 초보 요리사 추천")
    beginner = recipes.get("beginner", [])
    if beginner:
        _render_recipe_cards(beginner, owned)
    else:
        st.info("재료가 부족해요. 더 많은 재료를 추가해보세요.")

    st.markdown("---")

    st.markdown("## 전자레인지 간편 요리")
    microwave = recipes.get("microwave", [])
    if microwave:
        _render_recipe_cards(microwave, owned)
    else:
        st.info("재료가 부족해요. 더 많은 재료를 추가해보세요.")

    st.markdown("---")
    col_back, col_reset = st.columns([1, 1])
    if col_back.button("← 재료 보강으로"):
        st.session_state.step = 2
        st.rerun()
    if col_reset.button("처음부터 다시"):
        for k in ["ingredients", "sauces", "tools", "extra_ingredients", "recipes"]:
            st.session_state[k] = [] if k != "recipes" else {}
        st.session_state.step = 0
        st.rerun()


def _render_recipe_cards(recipe_list: list, owned: set):
    cols = st.columns(min(len(recipe_list), 3))
    for i, recipe in enumerate(recipe_list[:3]):
        with cols[i]:
            difficulty = recipe.get("difficulty", 1)
            have = [r for r in recipe["ingredients"] if r in owned]
            missing = [r for r in recipe["ingredients"] if r not in owned]

            with st.container(border=True):
                st.markdown(f"### {recipe['name']}")
                st.markdown(f"난이도: **{DIFFICULTY_LABEL[difficulty]}** &nbsp;|&nbsp; 시간: {recipe['time']}")
                st.markdown(f"_{recipe['summary']}_")

                st.markdown("**재료**")
                if have:
                    st.markdown(" ".join(f"`{r}`" for r in have))
                if missing:
                    st.markdown(
                        " ".join(
                            f'<span style="background:#dbeafe;padding:2px 6px;border-radius:4px;font-size:0.85em;color:#1d4ed8">{r}</span>'
                            for r in missing
                        ),
                        unsafe_allow_html=True,
                    )
                    st.caption(f"없는 재료: {', '.join(missing)}")
