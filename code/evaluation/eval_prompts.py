def qa_prompt_from_questions(artifact_id, description, questions):
    # Format questions in display form
    questions_str = "\n".join([f"- {q}" for q in questions])

    # Format answers JSON structure dynamically
    answers_block = ",\n".join([
        f'''{{\n      "question": "{q}",\n      "answer": "Answer to this question."\n    }}'''
        for q in questions
    ])

    prompt = f"""
        You are a knowledgeable and engaging museum guide at the Metropolitan Museum of Art.
        
        You will be given:
        - An artifact description (background).
        - A list of visitor follow-up questions.
        
        Your task:
        1. Write a concise and informative **introduction** (3–5 sentences) about the artifact, suitable for a live museum tour.
        2. Then, answer each **visitor question** one by one, based on the background and logical inference.
        3. Your responses must:
           - Be **factually accurate**
           - Be **direct and relevant** to the question
           - Use **clear and engaging language**
           - Maintain **conversational coherence** across all responses
           - **Avoid repeating information** already stated in the introduction or prior answers
        
        Return your response in this JSON format:
        
        {{
          "artifact_id": "{artifact_id}",
          "introduction": "Your 3–5 sentence summary of the artifact.",
          "answers": [
            {answers_block}
          ]
        }}
        
        ### Artifact Description:
        \"\"\"
        {description}
        \"\"\"
        
        ### Visitor Questions:
        {questions_str}
        """
    return prompt

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

eval_criteria = [
        {
            "name": "Factual Accuracy",
            "description": "Check whether the guide's statements are historically and culturally accurate. Do not rely on simple keyword overlap. For example, '5,200 years ago' and '3200–3100 BCE' are equivalent. Penalize incorrect or misleading interpretations.",
            "instruction": "Score from 1 to 5:\n1 = Hallucinated or mostly incorrect\n3 = Some minor factual issues or vague details\n5 = Entirely accurate and historically grounded"
        },
        {
            "name": "Relevance and Responsiveness",
            "description": "Evaluate whether the guide directly and contextually answers the user’s follow-up questions. Responses should not be vague or generic.",
            "instruction": "Score from 1 to 5:\n1 = Irrelevant or ignores the user’s question\n3 = Partially relevant or overly generic\n5 = Direct, specific, and clearly answers the user’s intent"
        },
        {
            "name": "Clarity and Engagement",
            "description": "Assess how clear, fluent, and engaging the guide is. Tone should be informative but approachable — like a real museum guide.",
            "instruction": "Score from 1 to 5:\n1 = Confusing, robotic, or unnatural\n3 = Understandable but dull or awkward\n5 = Clear, concise, and engaging like a skilled guide"
        },
        {
            "name": "Conversational Coherence",
            "description": "Evaluate whether the guide maintains a logical flow, refers back to earlier points naturally (without repetition), and expands beyond the artifact when appropriate.",
            "instruction": "Score from 1 to 5:\n1 = Disjointed or redundant\n3 = Some inconsistencies or rigid responses\n5 = Smooth, natural flow with relevant callbacks or expansions"
        }
    ]

def generate_single_eval_prompt(background, previous_conversation, question, answer, reference_answer, evals):
    """
    - previous_conversation: string of previous Q&As ("" if evaluating introduction)
    - question: str (the current question, or "" if introduction)
    - answer: str (the system's answer to evaluate, or the introduction if question is "")
    - reference_answer: str (the reference/gold answer for this question)
    - eval_criteria: list of criteria dicts (as before)
    Returns: list of prompts, one for each evaluation aspect
    """
    prompts = []
    for criterion in evals:
        prompt = f"""###Task Description:
          A background, the previous conversation (if any), the current question and answer, a reference answer (ideal=score 5), and a score rubric are provided.
            
            1. Write a very brief, succinct (< 40 words max) feedback evaluating the quality of the **current answer** ONLY, strictly based on the criterion: **{criterion['name']}**.
            2. Use the background and the previous conversation for context if provided. If there is no previous conversation or question, treat the answer as an introduction.
            3. Score from 1 to 5, per the rubric.
            4. Format: "Feedback: {{your feedback}} [RESULT] {{1–5}}". Include [RESULT] and no other commentary.
            
            ###Background:
            {background}
            
            ###Previous Conversation:
            {previous_conversation if previous_conversation else '(None; this is the introduction)'}
            
            ###Current Question:
            {question}
            
            ###System Answer to Evaluate:
            {answer}
            
            ###Reference Answer (Score 5):
            {reference_answer}
            
            ###Evaluation Criterion: {criterion['description']}
            ###Scoring Rubric:
            {criterion['instruction']}
            
            ###Feedback:"""
        prompts.append({
            "aspect": criterion["name"],
            "prompt": prompt
        })
    return prompts