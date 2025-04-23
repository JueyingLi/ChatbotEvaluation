import requests
import urllib3
from config import DIFY_API_KEY
from code.helpers.sql_helper import get_data_by_id
from code.helpers.json_helpers import safe_json_parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DifyConnector:
    def __init__(self, item_id, user_id="abc-123"):
        self.round = 0
        self.item_id = item_id
        self.conversation_id = None
        self.user_id = user_id
        self.sql_table = "metv0.2"
        self.dify_api_url = "https://01a03eca7d38.ngrok.app/v1/"
        self.item_name = None
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DIFY_API_KEY}"
        }

    def _pack_info(self):
        fields = ["title", "artist", "culture", "date", "period", "medium",
                  "classification", "exhibition_loc", "introduction"]
        columns = ["Title", "Artist Display Name", "Culture", "Object Date", "Period", "Medium",
                   "Classification", "Gallery Number", "BasicIntro"]
        obj_info = get_data_by_id(self.sql_table, self.item_id, columns)
        if obj_info:
            self.item_name = obj_info[0].get("Title", "")
            return "\n".join(
                f"item_{field}: {obj_info[0][col]}" for field, col in zip(fields, columns)
            )
        return ""

    def _post_to_dify(self, query, language="English", memory=""):
        if self.round == 0:
            self.payload = {
                "inputs": {
                    "userLang": language,
                    "item_info": self._pack_info(),
                    "user_memory_input": memory
                },
                "query": query,
                "response_mode": "blocking",
                "user": self.user_id
            }
        else:
            self.payload["conversation_id"] = self.conversation_id
            self.payload["query"] = query

        res = requests.post(self.dify_api_url + "chat-messages", headers=self.headers, json=self.payload, verify=False)
        self.round += 1
        res_json = res.json()
        self.conversation_id = res_json.get("conversation_id")
        if res_json["answer"]:
            return safe_json_parse(res_json["answer"])["output"]
        return "No response"

    def ask_initial_question(self):
        return self._post_to_dify("Introduce this artifact.")

    def ask_follow_up(self, question, previous_questions):
        return self._post_to_dify(question, memory = previous_questions)
