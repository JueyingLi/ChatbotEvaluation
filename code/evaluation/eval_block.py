class EvalBlock:
    def __init__(self, title, gpt_response, custom_response, ratings, feedbacks):
        self.title = title
        self.gpt_response = gpt_response
        self.custom_response = custom_response
        self.ratings = ratings
        self.feedbacks = feedbacks

    def print_eval_block(self):
        print("Title:", self.title)
        print("GPT Response:", self.gpt_response)
        print("custom Response:", self.custom_response)
        print("Ratings:", str(self.ratings))
        print("Feedback:", str(self.feedbacks))