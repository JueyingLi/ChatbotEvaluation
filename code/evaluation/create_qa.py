from code.helpers.sql_helper import get_data_by_id
from code.helpers.gpt_helper import connect_to_gpt
from code.evaluation.eval_prompts import qa_prompt_from_questions
columns = ["Title", "Artist Display Name", "Culture", "Object Date", "Period", "Medium", "Classification", "Gallery Number", "BasicIntro"]

def create_qa_from_id(id, questions):
    sql_table = "metv0.2"
    obj_info = get_data_by_id(sql_table, id, columns)
    basic_intro = obj_info[0]['BasicIntro']
    return connect_to_gpt(qa_prompt_from_questions(id, basic_intro, questions), "")