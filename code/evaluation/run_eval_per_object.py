import streamlit as st
from code.evaluation.create_qa import create_qa_from_id
from code.evaluation.eval_prompts import generate_single_eval_prompt, eval_criteria
from code.helpers.gpt_helper import connect_to_gpt
from code.helpers.dify_helper import DifyConnector
from code.helpers.sql_helper import get_data_by_id
from code.helpers.json_helpers import parse_gpt_response_to_json
from .eval_block import EvalBlock

class AnswerEvaluation:
    def __init__(self, artifact_id, questions):
        self.artifact_id = artifact_id
        self.background = get_data_by_id("metv0.2", artifact_id, ['BasicIntro'])[0]
        self.qa_pair = parse_gpt_response_to_json(create_qa_from_id(artifact_id, questions), artifact_id)
        self.previous_conversation = ""
        self.dify_obj = DifyConnector(artifact_id)
        self.eval_blocks = []
        self.counter = 0

    def run_eval(self, question, answer, reference_response):
        prompts = generate_single_eval_prompt(self.background, self.previous_conversation, question, answer, reference_response, eval_criteria)
        feedbacks = []
        scores = []
        for i, prompt in enumerate(prompts):
            eval_result = connect_to_gpt("You are a fair evaluator language model. \n", prompt['prompt'])
            feedback, score = [item.strip() for item in eval_result.split("[RESULT]")]
            feedbacks.append(feedback)
            scores.append(int(score))
        eval_obj = EvalBlock(title=question, gpt_response=reference_response, custom_response=answer, ratings=scores, feedbacks=feedbacks
        )
        self.eval_blocks.append(eval_obj)

    def generate_intro(self):
        self.intro_dify = self.dify_obj.ask_initial_question()
        self.intro_gpt4 = self.qa_pair["introduction"]
        self.run_eval( "Introduction", self.intro_dify, self.intro_gpt4)
        self.previous_conversation += "Introduction: " + self.intro_dify + "\n"

    def generate_followup(self, i):
        i = i if i else self.counter
        ans_dify = self.dify_obj.ask_follow_up(self.qa_pair["answers"][i]["question"], self.previous_conversation)
        self.run_eval(self.qa_pair["answers"][i]["question"], ans_dify, self.qa_pair["answers"][i]["answer"])
        self.previous_conversation += "Q" + str(i) + ": " + self.qa_pair["answers"][i]["question"] + "\n" + "A" + str(i) + ": " + ans_dify + "\n"

    def get_intro_score(self):
        return self.intro_score

    def get_avg_followup_score(self):
        return self.followup_scores / len(self.followup_scores)

    def get_followup_scores(self):
        return self.followup_scores

    def eval_report(self):
        pass
        #print("Intro Score: ", self.intro_score, "\nFollowup Scores:", sum(self.followup_scores) / len(self.followup_scores))
        #print("Intro Feedback: " + self.intro_feedback)
        #print("followupFeedback: \n" + "\n\t".join(self.followup_feedbacks))

def run_eval_per_object_test(artifact_id, questions):
    artifact = AnswerEvaluation(artifact_id, questions)
    artifact.generate_intro()
    st.session_state.eval_blocks = artifact.eval_blocks
    for i in range(len(questions)):
        artifact.generate_followup(i)
        st.session_state.eval_blocks = artifact.eval_blocks
    artifact.eval_report()

'''
questions = [
        "What is the historical context of this artifact?",
        "Who created this object and why?",
        "What materials and techniques were used?",
    ]
run_eval_per_object_test(544067, questions)
'''