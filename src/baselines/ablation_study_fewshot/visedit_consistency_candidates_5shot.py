# few-shot setting
from modules.chatbot import ChatBot
from utils.get_schema import get_all_schema
import os
import json


from prompts.ablation_study_5shot.visedit_consistency_prompt import CLAUSE_LOCATION_PROMPT,SCHEMA_LINKING_PROMPT, GENERATION_PROMPT, MERGE_PROMPT

schema_linking_template={
    "reason": "(your rationale for the potential database schema links, as a text)",
    "answer": "(the potential database schema links, as a text)"
}

clause_location_template={
    "reason": "(your rationale for the wrong clause, as a text)",
    "answer": "(the wrong clause, as a text)"
}

generation_template={
    "reason": "(your rationale for the generated clause, as a text)",
    "answer": "(your generated clause, as a text)"
}

merge_template={
    "reason": "(your rationale for the generated data visualization query, as a text)",
    "answer": "(your data visualization query, as a text)"
}


SCHEMA_LINKING_USER_PROMPT="""
You will be given a user utterance, the associated database schema, an incorrect data visualization query and the corresponding guidance that helps you correct the incorrect data visualization query to the correct one.
The 'user utterance' is a natural language text describing the requirement of user. The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to identify the potential database schema links which will be used to correct the incorrect data visualization query, given the database schema, the incorrect data visualization query and the corresponding guidance.

Provide your answer in JSON format as follows:

Answer:
{template}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the database schema, the user utterance, incorrect data visualization query and the guidance.

SQLite SQL tables, with their properties:\n{schema}\n
User utterance: {question}\n
Incorrect data visualization query: {err_query}\n
Guidance on the incorrect data visualization query: {feedback}\n
Answer: """


CLAUSE_LOCATION_USER_PROMPT="""
You will be given a user utterance, the potential database schema links, an incorrect data visualization query and the corresponding guidance that helps you correct the incorrect query to the correct one.
The 'user utterance' is a natural language text describing the requirement of user. The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to detect the wrong clauses of the incorrect data visualization query, given the user utterance, the database schema, the incorrect data visualization query and the guidance. Please note that there may be one or more wrong clauses.

Provide your answer in JSON format as follows:

Answer:
{template}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the database schema, the user utterance, data visualization query and the guidance.

SQLite SQL schema links:\n{schema_links}\n
User utterance: {question}\n
Incorrect data visualization query: {err_query}\n
Guidance on the incorrect query: {feedback}\n
Answer: """


GENERATION_USER_PROMPT="""
You will be given a user utterance, the potential database schema links, an incorrect data visualization query, the identified wrong clauses, the corresponding guidance that helps you correct the incorrect query to the correct one.

The 'user utterance' is a natural language text describing the requirement of user. The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to generate the correct clause, given the user utterance, the database schema, the incorrect data visualization query, the identified wrong clauses, and the guidance.

Provide your answer in JSON format as follows:

Answer:
{template}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the database schema, the user utterance, the incorrect data visualization query and the guidance.

SQLite SQL schema links:\n{schema_links}\n
User utterance: {question}\n
Incorrect data visualization query: {err_query}\n
Wrong clauses: {wrong_clause}\n
Guidance on the incorrect query: {feedback}\n
Answer: """


MERGE_USER_PROMPT="""
You will be given an incorrect data visualization query, the identified wrong clause, the correct clause and the corresponding guidance that helps you correct the incorrect query to the correct one.
The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to correct the incorrect data visualiation query, given the wrong clause, the correct clause and the guidance.

Provide your answer in JSON format as follows:

Answer:
{template}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the incorrect data visualization query, the identified wrong clause, the corresponding clauses and the guidance.

Incorrect data visualization query: {err_query}\n
Wrong clause: {wrong_clause}\n
Correct clause: {correct_clause}\n
Guidance on the incorrect query: {feedback}\n
Answer: """


from collections import Counter

def most_frequent_string(string_list):
    if not string_list:
        return None  # Return None if the list is empty

    # Count the frequency of each string
    frequency = Counter(string_list)

    # Find the string with the maximum frequency
    max_string = max(frequency, key=frequency.get)

    return max_string

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
            "temperature":0.7,  # do_sample=False, and ignore the temperature.
            "top_p":0.9,
        }

        self.pipeline_gen_candidates_kwargs = {
            "max_new_tokens":512,
            "eos_token_id":self.terminators,
            "do_sample":True,
            "temperature":0.7,  # do_sample=False, and ignore the temperature.
            "top_p":0.9,
        }

        # self.sys_msg = self._build_sys_msg(n=args.num_examples)


    def generate(self, args, df_row):
        question = df_row["question"]
        err_query = df_row["prediction"]
        feedback = df_row["feedback"]
        # gt_query = df_row["tokenized_query"]
        db_id = df_row["db_id"]
        schema = get_all_schema(db_path=os.path.join(args.db_path, f"{db_id}/{db_id}.sqlite")) 

        # Candidate Generation
        query_candidates = []
        for _ in range(self.args.top_k):
            # schema linking
            user_prompt_schema_linking = SCHEMA_LINKING_USER_PROMPT.format(question=question, err_query=err_query, schema=schema, feedback=feedback, template=json.dumps(schema_linking_template))
            messages = [
            {"role": "system", "content": SCHEMA_LINKING_PROMPT},
            {"role": "user", "content": user_prompt_schema_linking},
            ]
            # schema_links = self.chatbot.chat(messages, **self.pipeline_kwargs)
            schema_links = self.chatbot.chat(messages, **self.pipeline_gen_candidates_kwargs)

            # clause location
            user_prompt_clause_location = CLAUSE_LOCATION_USER_PROMPT.format(question=question, err_query=err_query, feedback=feedback, schema_links=schema_links, template=json.dumps(clause_location_template))
            messages = [
            {"role": "system", "content": CLAUSE_LOCATION_PROMPT},
            {"role": "user", "content": user_prompt_clause_location},
            ]
            # wrong_clause = self.chatbot.chat(messages, **self.pipeline_kwargs)
            wrong_clause = self.chatbot.chat(messages, **self.pipeline_gen_candidates_kwargs)

            # clause generation
            user_prompt_clause_generation = GENERATION_USER_PROMPT.format(question=question, err_query=err_query, schema_links=schema_links, wrong_clause=wrong_clause, feedback=feedback, template=json.dumps(generation_template))
            clause_generation_msg = [
            {"role": "system", "content": GENERATION_PROMPT},
            {"role": "user", "content": user_prompt_clause_generation},
            ]
            correct_clause = self.chatbot.chat(clause_generation_msg, **self.pipeline_gen_candidates_kwargs)
            
            # merge
            user_prompt_merge = MERGE_USER_PROMPT.format(err_query=err_query, wrong_clause=wrong_clause, correct_clause=correct_clause, feedback=feedback, template=json.dumps(merge_template))
            messages = [
            {"role": "system", "content": MERGE_PROMPT},
            {"role": "user", "content": user_prompt_merge},
            ]
            # query = self.chatbot.chat(messages, **self.pipeline_kwargs)
            query = self.chatbot.chat(messages, **self.pipeline_gen_candidates_kwargs)
            try:
                assert type(query)==str
            except:
                query = "Error."
            query_candidates.append(query)

        # candidate selection
        # answer = most_frequent_string(query_candidates)        
        
        return query_candidates