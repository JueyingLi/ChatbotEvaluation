from code.evaluation.create_qa import create_qa_from_id
from code.evaluation.eval_prompts import eval_prompt
from code.helpers.gpt_helper import connect_to_gpt
from code.helpers.dify_helper import DifyConnector
from code.helpers.sql_helper import get_data_by_id
from code.helpers.json_helpers import parse_gpt_response_to_json

class AnswerEvaluation:
    def __init__(self, artifact_id):
        self.artifact_id = artifact_id
        self.background = get_data_by_id("metv0.2", artifact_id, ['BasicIntro'])[0]
        self.qa_pair = parse_gpt_response_to_json(create_qa_from_id(artifact_id), artifact_id)
        print(self.qa_pair)
        self.dify_obj = DifyConnector(artifact_id)
        self.intro_dify = None
        self.intro_gpt4 = None
        self.intro_score = None
        self.followup_scores = []
        self.followup_feedbacks = []
        self.counter = 0

    def run_eval(self, question, answer, reference_response):
        eval_result = connect_to_gpt("You are a fair evaluator language model. \n",
                                     eval_prompt(self.background, question, answer, reference_response))
        feedback, score = [item.strip() for item in eval_result.split("[RESULT]")]
        return int(score), feedback

    def generate_intro(self):
        self.intro_dify = self.dify_obj.ask_initial_question()
        self.intro_gpt4 = self.qa_pair["introduction"]
        score, feedback = self.run_eval( "Introduce this artifact", self.intro_dify, self.intro_gpt4)
        self.intro_score = score
        self.intro_feedback = feedback
        print(self.intro_score, self.intro_feedback)

    def generate_followup(self, i):
        i = i if i else self.counter
        ans_dify = self.dify_obj.ask_follow_up(self.qa_pair["questions"][i]["question"])
        print("\nQuestion: " + self.qa_pair["questions"][i]["question"])
        print("\tgpt-4: " + self.qa_pair["questions"][i]["answer"])
        print("\tdify: " + ans_dify)
        score, feedback = self.run_eval(self.qa_pair["questions"][i]["question"], ans_dify, self.qa_pair["questions"][i]["answer"])
        self.followup_scores.append(score)
        self.followup_feedbacks.append(feedback)

    def get_intro_score(self):
        return self.intro_score

    def get_avg_followup_score(self):
        return self.followup_scores / len(self.followup_scores)

    def get_followup_scores(self):
        return self.followup_scores

    def eval_report(self):
        print("Intro Score: ", self.intro_score, "\nFollowup Scores:", sum(self.followup_scores) / len(self.followup_scores))
        print("Intro Feedback: " + self.intro_feedback)
        print("followupFeedback: \n" + "\n\t".join(self.followup_feedbacks))

def run_eval_per_object_test(artifact_id):
    artifact = AnswerEvaluation(artifact_id)
    artifact.generate_intro()
    artifact.generate_followup(0)
    artifact.generate_followup(1)
    artifact.generate_followup(2)
    artifact.eval_report()


run_eval_per_object_test(544067)