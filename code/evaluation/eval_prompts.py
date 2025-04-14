
def qa_prompt(artifact_id, description):
    qa_prompt = f"""
                You are given a museum artifact description. Your task is to:
                
                1. Write a clear and engaging **introduction** (3–5 sentences) summarizing the artifact.
                2. Generate **three questions**:
                   - Two questions should be **answerable from the text**.
                   - One question should require **external cultural, historical, or artistic knowledge**.
                3. Provide **answers** to all three questions and indicate the **source** of each answer:
                   - Use `"text"` if the answer comes from the original description.
                   - Use `"external"` if it requires outside knowledge.
                
                Return your response in the following JSON format:
                
                {{
                  "artifact_id": "{artifact_id}",
                  "introduction": "Your 3–5 sentence summary here.",
                  "questions": [
                    {{
                      "question": "First question based on the text.",
                      "answer": "Answer to first question.",
                      "answer_source": "text"
                    }},
                    {{
                      "question": "Second question based on the text.",
                      "answer": "Answer to second question.",
                      "answer_source": "text"
                    }},
                    {{
                      "question": "Third question requiring external knowledge.",
                      "answer": "Answer to third question.",
                      "answer_source": "external"
                    }}
                  ]
                }}
                
                Artifact Description:
                \"\"\"
                {description}
                \"\"\"
                """
    return qa_prompt

def eval_prompt(background, question, response, reference_answer):
    eval_prompt = f"""###Task Description:
    A background, a question, a response to that question based on the background to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
    1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
    2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric.
    3. The output format should look as follows: \"Feedback: {{write a feedback for criteria}} [RESULT] {{an integer number between 1 and 5}}\"
    4. Please do not generate any other opening, closing, and explanations. Be sure to include [RESULT] in your output.

    ###The background information:
    {background}

    ###The question to the response answer to:
    {question}

    ###Response to evaluate:
    {response}

    ###Reference Answer (Score 5):
    {reference_answer}

    ###Score Rubrics:
    [Is the response correct, accurate, and factual based on the reference answer?]
    Score 1: The response is completely incorrect, inaccurate, and/or not factual.
    Score 2: The response is mostly incorrect, inaccurate, and/or not factual.
    Score 3: The response is somewhat correct, accurate, and/or factual.
    Score 4: The response is mostly correct, accurate, and factual.
    Score 5: The response is completely correct, accurate, and factual.

    ###Feedback:"""
    return eval_prompt