from modules.chatbot import ChatBot
from utils.get_schema import get_all_schema
import os
import json

USER_PROMPT="""
You will be given a user utterance, the associated database schema, an incorrect data visualization query and the corresponding guidance that helps you correct the incorrect query to the correct one.
The 'user utterance' is a natural language text describing the requirement of user. The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to correct the incorrect data visualiation query, given the user utterance, the database schema and the guidance.

Provide your answer in JSON format as follows:

Answer:
{template}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the database schema, the user utterance, data visualization query and the guidance.

SQLite SQL tables, with their properties:\n{schema}\n
User utterance: {question}\n
Incorrect data visualization query: {err_query}\n
Guidance on the incorrect query: {feedback}\n
Answer: """


class Model:
    def __init__(self, args) -> None:
        self.args = args
        self.chatbot = ChatBot(model_id=args.model_id)
        self.terminators = [
            self.chatbot.pipeline.tokenizer.eos_token_id,
            self.chatbot.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        self.pipeline_kwargs = {
            "max_new_tokens":512,
            "eos_token_id":self.terminators,
            "do_sample":False,
            "temperature":0.001,  # do_sample=False, and ignore the temperature.
            "top_p":0.9,
        }


    def generate(self, args, df_row):
        question = df_row["question"]
        err_query = df_row["prediction"]
        feedback = df_row["feedback"]
        # gt_query = df_row["tokenized_query"]
        db_id = df_row["db_id"]
        schema = get_all_schema(db_path=os.path.join(args.db_path, f"{db_id}/{db_id}.sqlite")) 

        template={
            "reason": "(your rationale for the guidance, as a text)",
            "answer": "(your data visualization query, as a text)"
            }
        user_prompt = USER_PROMPT.format(question=question, err_query=err_query, feedback=feedback, schema=schema, template=json.dumps(template))

        messages = [
        {"role": "system", "content": ""},
        {"role": "user", "content": user_prompt},
        ]
        # print(user_prompt)
        return self.chatbot.chat(messages, **self.pipeline_kwargs)