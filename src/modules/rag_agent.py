import transformers
import torch
import json
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document as LangchainDocument

from prompts.system_msg_correct_query import EVALUATION_PROMPT
from prompts.system_msg_editops import GEN_EDITOPS_PROMPT
from prompts.zero_shot import ZERO_SHOT_PROMPT
from prompts.one_pass_random_icl_prompt import ONE_PASS_RANDOM_ICL_PROMPT
from prompts.multi_round_random_icl_prompt import MULTI_ROUND_RANDOM_ICL_IR_PROMPT, MULTI_ROUND_RANDOM_ICL_EVALUATION_PROMPT
from prompts.multi_round_user_prompt import GEN_IR_USER_PROMPT, GEN_IR_QUERY_USER_PROMPT
from utils.get_schema import get_all_schema


user_prompt_template = """
{schema}
Error query: {err_query}
User intent: {question}
Question: {feedback}
Answer: """

class Retriever:
    def __init__(self, df_data, search_kwargs={"k": 10}, key_content=None, model_id="sentence-transformers/all-MiniLM-l6-v2") -> None:
        print("Load data into Vector DB:")
        self.data = self.pre_process(df_data, key_content)
        # print(data[0])

        # Create a dictionary with model configuration options, specifying to use the CPU for computations
        model_kwargs = {'device':'cuda'}
        # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
        encode_kwargs = {'normalize_embeddings': False}

        # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_id,     # Provide the pre-trained model's path
            model_kwargs=model_kwargs, # Pass the model configuration options
            encode_kwargs=encode_kwargs # Pass the encoding options
        )

        self.db = FAISS.from_documents(self.data, self.embeddings)
        self.retriever = self.db.as_retriever(search_kwargs=search_kwargs)

    def pre_process(self, df_data:pd.DataFrame, key_content):
        if key_content is not None:
            return [LangchainDocument(page_content=row[key_content], metadata={"question": row["question"], "err_query": row["prediction"], "feedback": row["llm_feedback"], "db_id": row["db_id"], "gt_query":row["tokenized_query"]}) for _, row in tqdm(df_data.iterrows())]
        else:
            return [LangchainDocument(page_content=row["question"]+row["prediction"]+row["llm_feedback"], metadata={"question": row["question"], "err_query": row["prediction"], "feedback": row["llm_feedback"], "db_id": row["db_id"], "gt_query":row["tokenized_query"]}) for _, row in tqdm(df_data.iterrows())]
    

    def get_top_k(self, query:str):
        return self.retriever.get_relevant_documents(query)
    
    def get_random_top_k(self, k=10):
        num_random_samples = k
        random_indices = np.random.choice(len(self.data), num_random_samples, replace=False)

        # Retrieve examples
        examples = [self.data[int(i)] for i in random_indices]

        return examples


def get_user_msg(question, err_query, feedback, schema=""):
    prompt = user_prompt_template.format(schema=schema,question=question,err_query=err_query,feedback=feedback)
    return prompt

class Agent:
    def __init__(self, args) -> None:
        self.db_path = args.db_path
        self.model_id = args.model_id
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )
        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]


    def generator(self, messages:list):
        outputs = self.pipeline(
            messages,
            max_new_tokens=512,
            eos_token_id=self.terminators,
            do_sample=False,
            temperature=0.001,  # do_sample=False, and ignore the temperature.
            top_p=0.9,
        )

        # output = outputs[0]["generated_text"][-1]
        # try:
        #     json_data = json.loads(output["content"])
        #     pred = json_data["answer"]
        # except:
        #     pred = "Error."
        output_dict = outputs[0]["generated_text"][-1]
        output_text = output_dict["content"]
        # print(output_text)
        try:
            pred = json.loads(output_text)["answer"]
        except:
            try:
                beg = output_text.index("{")
                end = output_text.rindex("}")
                pred = json.loads(output_text[beg:end+1])["answer"]
            except:
                pred = "error."
                # err_cnt += 1
        
        return pred
    
    def gen_query_zero_shot(self, question, err_query, feedback, schema):
        template={
        "reason": "(your rationale for the guidance, as a text)",
        "answer": "(your data visualization query, as a text)"
        }
        user_prompt = ZERO_SHOT_PROMPT.format(question=question, err_query=err_query, feedback=feedback, schema=schema, template=json.dumps(template))
        # print(user_prompt)
        messages = [
        {"role": "system", "content": """Generate the visualization query given the error query and the corrsponding user intent.  When answering user questions follow these examples. Your response should be in JSON format template: {"reason":"(your rationale for the guidance, as a text)","answer": "(your answer query, as a text)"}"""},
        {"role": "user", "content": user_prompt},
        ]
        # print(user_prompt)
        return self.generator(messages)

    def gen_query_basic_cot(self, question, err_query, feedback, schema):
        template={
        "reason": "(your rationale for the guidance, as a text)",
        "answer": "(your data visualization query, as a text)"
        }
        user_prompt = ZERO_SHOT_PROMPT.format(question=question, err_query=err_query, feedback=feedback, schema=schema, template=json.dumps(template))
        messages = [
        {"role": "system", "content": ONE_PASS_RANDOM_ICL_PROMPT},
        {"role": "user", "content": user_prompt},
        ]

        return self.generator(messages)
    
    def gen_query_editops_cot(self, question, err_query, feedback, schema):
        template_1={
        "reason": "(your rationale for generating edit operations, as a text)",
        "answer": "(your edit operations, as a text)"
        }
        user_prompt_1 = GEN_IR_USER_PROMPT.format(question=question, err_query=err_query, feedback=feedback, schema=schema, template=json.dumps(template_1))
        messages = [
        {"role": "system", "content": MULTI_ROUND_RANDOM_ICL_IR_PROMPT},
        {"role": "user", "content": user_prompt_1},
        ]
        edit_ops = self.generator(messages)

        # query
        template_2={
        "answer": "(your data visualization query, as a text)"
        }
        user_prompt_2 = GEN_IR_QUERY_USER_PROMPT.format(template=template_2, err_query=err_query, editops=edit_ops)
        messages = [
        {"role": "system", "content": MULTI_ROUND_RANDOM_ICL_EVALUATION_PROMPT},
        {"role": "user", "content": user_prompt_2},
        ]

        return self.generator(messages)
    

    def get_similar_prompt(self, key_content, retriever:Retriever):
        few_shot_examples = ""
        similar_examples = retriever.get_top_k(key_content)
        for example in similar_examples:
            metadata = example.metadata
            question = metadata["question"]
            err_query = metadata["err_query"]
            feedback = metadata["feedback"]
            gt_query = metadata["gt_query"]
            db_id = metadata["db_id"]
            schema = get_all_schema(db_path=os.path.join(self.db_path, f"{db_id}/{db_id}.sqlite"))

            messages = [
            {"role": "system", "content": GEN_EDITOPS_PROMPT},
            {"role": "user", "content": get_user_msg(question, err_query, feedback, schema)},
            ]
            edit_ops = self.generator(messages)
            ans = {"answer": gt_query}
            text = f"""{schema}
            Error query: {err_query}
            User intent: {question}
            Question: {edit_ops}
            Answer: {json.dumps(ans)} \n\n"""
            few_shot_examples += text

        json_template = {"answer": ""}
        rag_prompt = f"""Generate the visualization query given the error query and the corrsponding user intent.  When answering user questions follow these examples. Your response should be in JSON format template: {json.dumps(json_template)}.

        {few_shot_examples}
        """

        # print(rag_prompt)
        return rag_prompt
    
    def get_random_prompt(self, retriever:Retriever):
        few_shot_examples = ""
        similar_examples = retriever.get_random_top_k()
        for example in similar_examples:
            metadata = example.metadata
            question = metadata["question"]
            err_query = metadata["err_query"]
            feedback = metadata["feedback"]
            gt_query = metadata["gt_query"]
            db_id = metadata["db_id"]
            schema = get_all_schema(db_path=os.path.join(self.db_path, f"{db_id}/{db_id}.sqlite"))

            messages = [
            {"role": "system", "content": GEN_EDITOPS_PROMPT},
            {"role": "user", "content": get_user_msg(question, err_query, feedback, schema)},
            ]
            edit_ops = self.generator(messages)
            ans = {"answer": gt_query}
            text = f"""{schema}
            Error query: {err_query}
            User intent: {question}
            Question: {edit_ops}
            Answer: {json.dumps(ans)} \n\n"""
            few_shot_examples += text

        json_template = {"answer": ""}
        rag_prompt = f"""Generate the visualization query given the error query and the corrsponding user intent.  When answering user questions follow these examples. Your response should be in JSON format template: {json.dumps(json_template)}.

        {few_shot_examples}
        """

        # print(rag_prompt)
        return rag_prompt



    def gen_query_editops_cot_rag(self, question, err_query, feedback, schema, retriever:Retriever, is_random=False):
        messages = [
        {"role": "system", "content": GEN_EDITOPS_PROMPT},
        {"role": "user", "content": get_user_msg(question, err_query, feedback, schema)},
        ]
        edit_ops = self.generator(messages) 

        # retrieval model
        key_content = question+err_query+feedback
        if is_random:
            evaluation_prompt = self.get_random_prompt(retriever)
        else:
            evaluation_prompt = self.get_similar_prompt(key_content, retriever)

        # query
        messages = [
        {"role": "system", "content": evaluation_prompt},
        {"role": "user", "content": get_user_msg(question, err_query, edit_ops, schema)},
        ]

        return self.generator(messages)
    
    def refiner_dinsql(self,question, err_query, feedback, schema, raw_output):
        pass
