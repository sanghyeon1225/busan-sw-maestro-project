import streamlit as st

DIFFICULTY_STARS = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}
DIFFICULTY_LABEL = {1: "매우 쉬움", 2: "쉬움", 3: "보통", 4: "어려움", 5: "매우 어려움"}


def render():
    st.title("🍳 Step 3 — 레시피 추천")
    st.markdown("---")

    recipes = st.session_state.get("recipes", {})

    if not recipes:
        st.warning("아직 레시피가 없어요! Step 2에서 재료 보강 후 레시피를 생성해주세요.")
        return

    owned = {i["name"] for i in st.session_state.get("ingredients", [])}
    owned |= set(st.session_state.get("sauces", []))
    owned |= set(st.session_state.get("extra_ingredients", []))

    # 초보 추천
    st.markdown("## 🔰 초보 요리사에게 추천해요!")
    beginner = recipes.get("beginner", [])
    if beginner:
        _render_recipe_cards(beginner, owned)
    else:
        st.info("재료가 부족해요! 더 많은 재료를 추가해보세요.")

    st.markdown("---")

    # 전자레인지
    st.markdown("## ⚡ 전자레인지로 만드는 간편 요리!")
    microwave = recipes.get("microwave", [])
    if microwave:
        _render_recipe_cards(microwave, owned)
    else:
        st.info("재료가 부족해요! 더 많은 재료를 추가해보세요.")

    st.markdown("---")
    if st.button("🔄 처음부터 다시", use_container_width=True):
        st.session_state.ingredients = []
        st.session_state.sauces = []
        st.session_state.tools = []
        st.session_state.extra_ingredients = []
        st.session_state.recipes = {}
        st.info("👈 사이드바에서 Step 1로 이동하세요!")


def _render_recipe_cards(recipe_list: list, owned: set):
    cols = st.columns(min(len(recipe_list), 3))
    for i, recipe in enumerate(recipe_list[:3]):
        with cols[i]:
            difficulty = recipe.get("difficulty", 1)
            have = [r for r in recipe["ingredients"] if r in owned]
            missing = [r for r in recipe["ingredients"] if r not in owned]

            with st.container(border=True):
                st.markdown(f"### {recipe['name']}")
                st.markdown(
                    f"{DIFFICULTY_STARS[difficulty]} **{DIFFICULTY_LABEL[difficulty]}** &nbsp;|&nbsp; ⏱️ {recipe['time']}"
                )
                st.markdown(f"_{recipe['summary']}_")

                st.markdown("**재료**")
                if have:
                    st.markdown(" ".join(f"`{r}`" for r in have))
                if missing:
                    st.markdown(
                        " ".join(
                            f'<span style="background:#fee2e2;padding:2px 6px;border-radius:4px;font-size:0.85em">{r}</span>'
                            for r in missing
                        ),
                        unsafe_allow_html=True,
                    )
                    st.caption(f"⚠️ 없는 재료: {', '.join(missing)}")
