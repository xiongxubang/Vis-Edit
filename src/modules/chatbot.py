import transformers
import torch
import json
import os
import pandas as pd
import numpy as np
from tqdm import tqdm


class ChatBot:
    def __init__(self, model_id) -> None:
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )
        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]


    def chat(self, messages:list, **pipeline_kwargs: dict):
        outputs = self.pipeline(
            messages,
            **pipeline_kwargs
        )

        output_dict = outputs[0]["generated_text"][-1]
        output_text = output_dict["content"]
        # print(output_text)
        try:
            prediction = json.loads(output_text)["answer"]
        except:
            try:
                beg = output_text.index("{")
                end = output_text.rindex("}")
                prediction = json.loads(output_text[beg:end+1])["answer"]
            except:
                prediction = "Error."
        
        return prediction
    

    def chat_json(self, messages:list, **pipeline_kwargs: dict):
        outputs = self.pipeline(
            messages,
            **pipeline_kwargs
        )

        output_dict = outputs[0]["generated_text"][-1]
        output_text = output_dict["content"]
        # print(output_text)
        try:
            prediction = json.loads(output_text)
        except:
            try:
                beg = output_text.index("{")
                end = output_text.rindex("}")
                prediction = json.loads(output_text[beg:end+1])
            except:
                prediction = {
                    "reason": "",
                    "answer": ""
                }
        
        return prediction
    
    