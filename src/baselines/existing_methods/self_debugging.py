from modules.chatbot import ChatBot
from utils.get_schema import get_all_schema
import os
import json
import pandas as pd

template={
            "answer": "(your generated VQL, as a text)"
            }

example_format = """
{schema}
Question: {question}
VQL: {prediction}
{prediction_expl}
Feedback: {feedback}
Answer: 
{answer}

"""

USER_PROMPT="""
Your task is to translate the following question into VQL.

The information of the keyword of the 'VQL' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Provide your answer in JSON format as follows:

Answer:
{template}

{schema}
Question: {question}
VQL: {prediction}
{prediction_expl}
Feedback: {feedback}
"""


SYSTEM_PROMPT="""
Your task is to translate the following question into VQL.

The information of the keyword of the 'VQL' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Provide your answer in JSON format as follows:

Answer:
{template}

{examples}
"""


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

        self.sys_msg = self._build_sys_msg(n=args.num_examples)


    def _build_sys_msg(self, n):
        train_data = pd.read_csv(self.args.train_data)
        samples = train_data.sample(n=n,random_state=1234,axis=0) 
        demonstrations = []
        for _,df_row in samples.iterrows():
            # print(type(df_row))
            question = df_row["question"]
            err_query = df_row["prediction"]
            feedback = df_row["feedback"]
            gt_query = df_row["tokenized_query"]
            db_id = df_row["db_id"]
            prediction_expl = df_row["wrong_explanation"]
            schema = get_all_schema(db_path=os.path.join(self.args.db_path, f"{db_id}/{db_id}.sqlite")) 
            answer = {"answer":gt_query}

            text = example_format.format(schema=schema,question=question, prediction=err_query,feedback=feedback, prediction_expl=prediction_expl, answer=json.dumps(answer))
            demonstrations.append(text)

        sys_msg = SYSTEM_PROMPT.format(template=template, examples="".join(demonstrations))
        return sys_msg


    def generate(self, args, df_row):
        question = df_row["question"]
        err_query = df_row["prediction"]
        feedback = df_row["feedback"]
        prediction_expl = df_row["wrong_explanation"]
        db_id = df_row["db_id"]
        schema = get_all_schema(db_path=os.path.join(args.db_path, f"{db_id}/{db_id}.sqlite")) 

        user_prompt = USER_PROMPT.format(question=question, prediction=err_query, feedback=feedback, schema=schema, prediction_expl=prediction_expl, template=json.dumps(template))

        messages = [
        {"role": "system", "content": self.sys_msg},
        {"role": "user", "content": user_prompt},
        ]
    
        return self.chatbot.chat(messages, **self.pipeline_kwargs)