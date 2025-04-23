import streamlit as st

def render_eval_block_object(eval_obj, eval_criteria):
    with st.expander(eval_obj.title):
        col1, col2 = st.columns([2, 2])
        with col1:
            st.header("GPT")
            st.write(eval_obj.gpt_response)
        with col2:
            st.header("Custom")
            st.write(eval_obj.custom_response)

        if eval_obj.ratings and eval_obj.feedbacks and len(eval_obj.ratings) == len(eval_criteria):
            st.markdown("#### Evaluation Summary")
            for i, criterion in enumerate(eval_criteria):
                crit_col, score_col, fb_col = st.columns([1.5, 1, 3])
                with crit_col:
                    st.markdown(f"**{criterion['name']}**")
                with score_col:
                    st.write(f"**Score:** {eval_obj.ratings[i]}")
                with fb_col:
                    st.write(eval_obj.feedbacks[i])
