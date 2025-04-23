import streamlit as st
from code.evaluation.run_eval_per_object import run_eval_per_object_test
from code.evaluation.eval_prompts import eval_criteria
from code.st_helpers.st_eval_block import render_eval_block_object

def render_evaluation_criteria(left_col, eval_criteria):
    for prompt in eval_criteria:
        with st.expander(prompt["name"]):
            st.markdown(f"**Description:** {prompt['description']}")
            st.write(f"**How to Score:**\n{prompt['instruction']}")

st.set_page_config(layout="wide")
# Init
if "questions" not in st.session_state:
    st.session_state.questions = [
        "What is the historical context of this artifact?",
        "Who created this object and why?",
        "What materials and techniques were used?",
    ]
if "intro" not in st.session_state:
    st.session_state.intro = ""

col1, spacer, col2 = st.columns([1.2, 0.2, 2])  # Adjust ratio as needed

# 🧾 Left column: question list and controls
with col1:
    st.header("📝 Questions")
    new_question = st.text_input("Add a new question:")
    if st.button("Add Question") and new_question:
        st.session_state.questions.append(new_question)

    for i, q in enumerate(st.session_state.questions):
        col_q1, col_q2, col_q3 = st.columns([6, 1, 1])
        col_q1.write(f"{i+1}. {q}")
        if col_q2.button("⬆️", key=f"up_{i}") and i > 0:
            st.session_state.questions[i-1], st.session_state.questions[i] = (
                st.session_state.questions[i],
                st.session_state.questions[i-1],
            )
        if col_q3.button("🗑️", key=f"del_{i}"):
            st.session_state.questions.pop(i)

    st.header("📝 Evaluation Metrics")
    render_evaluation_criteria(col1, eval_criteria)
# 💬 Right column: placeholder for future GPT response
with col2:
    st.header("MET LLM Chatbot Simulation")
    new_obj_id = st.text_input("Input an object ID")
    if st.button("Submit") and new_obj_id:
        run_eval_per_object_test(int(new_obj_id), st.session_state.questions)

    if st.session_state.get("eval_blocks"):
        for i in range(len(st.session_state.eval_blocks)):
            st.session_state.eval_blocks[i].print_eval_block()
            render_eval_block_object(st.session_state.eval_blocks[i], eval_criteria)