from run_eval_per_object import AnswerEvaluation
class AnswerEvaluationBatch:
    def __init__(self, ids):
        self.artifacts = [AnswerEvaluation(id) for id in ids]
        print(self.artifacts)
        self.avg_intro_score = None
        self.avg_followup_score = None

    def generate_batch_intro(self):
        for i in range(len(self.artifacts)):
            self.artifacts[i].generate_intro()

    def generate_batch_followup(self, count):
        for i in range(len(self.artifacts)):
            for j in range(count):
                self.artifacts[i].generate_followup(j)

    def run_batch_eval(self, count):
        self.generate_batch_intro()
        self.generate_batch_followup(3)
        self.avg_intro_score = sum([artifact.get_intro_score() for artifact in self.artifacts]) / len(self.artifacts)
        self.avg_followup_score = sum([artifact.get_avg_followup_score() for artifact in self.artifacts]) / len(self.artifacts)
        print("Batch Avg Intro Score: " + self.avg_intro_score)
        print("Batch Avg Followup Score: " + self.avg_followup_score)


artifactbatch = AnswerEvaluationBatch([543937, 544067])
print(type(artifactbatch))
artifactbatch.run_batch_eval(3)





