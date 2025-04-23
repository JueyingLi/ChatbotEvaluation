import streamlit as st

def render_question_list_editor():
    # --- Initialize session state ---
    if "raw_questions" not in st.session_state:
        st.session_state.raw_questions = "What is the historical context of this artifact?\nWho created this object and why?\nWhat materials and techniques were used?\n"
    if "questions" not in st.session_state:
        st.session_state.questions = ["What is the historical context of this artifact?", "Who created this object and why?", "What materials and techniques were used?"]

    # --- Input box ---
    st.markdown("Type or paste your questions below (one per line):")
    st.session_state.raw_questions = st.text_area(
        "Questions",
        st.session_state.raw_questions,
        height=200,
        key="question_input"
    )

    # --- Parse into list ---
    if st.button("Confirm"):
        st.session_state.questions = [
            q.strip() for q in st.session_state.raw_questions.strip().split("\n") if q.strip()
        ]