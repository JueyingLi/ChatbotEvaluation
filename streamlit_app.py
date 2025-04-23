import streamlit as st
from code.evaluation.run_eval_per_object import run_eval_per_object_test
from code.evaluation.eval_prompts import eval_criteria
from code.st_helpers.st_eval_block import render_eval_block_object
from code.st_helpers.st_question_ranking import render_question_list_editor

def render_evaluation_criteria(eval):
    for prompt in eval:
        with st.expander(prompt["name"]):
            st.markdown(f"**Description:** {prompt['description']}")
            st.write(f"**How to Score:**\n{prompt['instruction']}")

st.set_page_config(layout="wide")
# Init
col1, spacer, col2 = st.columns([1.2, 0.2, 2])  # Adjust ratio as needed
# 🧾 Left column: question list and controls
with col1:
    st.header("🔍 Questions")
    render_question_list_editor()

    st.header("📝 Evaluation Metrics")
    render_evaluation_criteria(eval_criteria)
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