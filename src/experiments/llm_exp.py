import pandas as pd
import os
from collections import Counter
from tqdm import tqdm
from experiments.basic_exp import BasicExp
# baselines
from baselines import visedit_consistency
from baselines.existing_methods import zero_shot, zero_shot_cot, random_few_shot, self_debugging
from baselines.ablation_study import visedit_consistency_wo_CL, visedit_consistency_wo_SC, visedit_consistency_wo_SL, visedit_consistency_candidates
from baselines.ablation_study_fewshot import visedit_consistency_wo_CL_5shot, visedit_consistency_wo_SC_5shot, visedit_consistency_wo_SL_5shot, visedit_consistency_candidates_5shot, visedit_consistency_wo_CL_10shot, visedit_consistency_wo_SC_10shot, visedit_consistency_wo_SL_10shot, visedit_consistency_candidates_10shot
from baselines.parameter_study import p_zero_shot, p_five_shot, p_ten_shot
# metrics
from evaluations.exact_match import is_match

def data_provider(args, flag)->pd.DataFrame:
    if flag == 'train':
        data_path = args.train_data
    elif flag == 'dev':
        data_path = args.dev_data
    else:
        data_path = args.test_data

    df_data = pd.read_csv(data_path)
    if args.num_data is not None:
        df_data = df_data[:args.num_data]
    
    print(f"The length of {flag} data: {len(df_data)}")
    return df_data


def most_frequent_string(string_list):
    if not string_list:
        return None  # Return None if the list is empty

    # Count the frequency of each string
    frequency = Counter(string_list)

    # Find the string with the maximum frequency
    max_string = max(frequency, key=frequency.get)

    return max_string

class LLMExp(BasicExp):
    def __init__(self, args):
        super().__init__(args)
        self.col_name = "raw_output"
        

    def _build_model(self):
        model_dict = {
            "zero_shot": zero_shot,
            "zero_shot_cot": zero_shot_cot,
            "random_few_shot": random_few_shot,
            "self_debugging": self_debugging,
            "visedit_consistency": visedit_consistency,
            "visedit_consistency_wo_CL": visedit_consistency_wo_CL,
            "visedit_consistency_wo_SC": visedit_consistency_wo_SC,
            "visedit_consistency_wo_SL": visedit_consistency_wo_SL,
            "visedit_consistency_candidates": visedit_consistency_candidates,
            "p_zero_shot": p_zero_shot,
            "p_five_shot": p_five_shot,
            "p_ten_shot": p_ten_shot,
            "visedit_consistency_k_5": visedit_consistency,
            "visedit_consistency_k_15": visedit_consistency,
            "visedit_consistency_k_20": visedit_consistency,
            "visedit_consistency_k_40": visedit_consistency_candidates,
            "visedit_consistency_wo_CL_5shot": visedit_consistency_wo_CL_5shot,
            "visedit_consistency_wo_SC_5shot": visedit_consistency_wo_SC_5shot,
            "visedit_consistency_wo_SL_5shot": visedit_consistency_wo_SL_5shot,
            "visedit_consistency_candidates_5shot": visedit_consistency_candidates_5shot,
            "visedit_consistency_wo_CL_10shot": visedit_consistency_wo_CL_10shot,
            "visedit_consistency_wo_SC_10shot": visedit_consistency_wo_SC_10shot,
            "visedit_consistency_wo_SL_10shot": visedit_consistency_wo_SL_10shot,
            "visedit_consistency_candidates_10shot": visedit_consistency_candidates_10shot,
        }
        model = model_dict[self.args.method].Model(self.args)
        return model
    

    def _get_data(self, flag):
        df_data = data_provider(self.args, flag)
        return df_data
    

    def _save_data(self, df_data, csv_name=None):
        if not os.path.exists(self.args.output_dir):
            os.system(f"mkdir -p {self.args.output_dir}")

        if csv_name is None:
            csv_path = os.path.join(self.args.output_dir, f"{self.args.method}.csv")
        else:
            csv_path = os.path.join(self.args.output_dir, f"{csv_name}.csv")
        df_data.to_csv(csv_path, index=False)
        print(f"df_data was saved in {os.path.abspath(csv_path)} sucessfully!")
        

    def test(self):
        em_cnt = 0
        df_data = self._get_data(flag='test')
        for index, df_row in tqdm(df_data.iterrows()):
            gold_query = df_row["tokenized_query"]
            prediction = self.model.generate(self.args, df_row)
            # print(prediction)
            df_data.loc[index, self.col_name] = prediction

            if is_match(prediction, gold_query):
                em_cnt += 1
            if (index+1) % 100 ==0:
                print(f"Exact Match:{em_cnt/(index+1) if (index+1)>0 else 0}")

        self._save_data(df_data)
        # exact match
        print(f"Data Length:{len(df_data)}")
        print(f"EM counter:{em_cnt}")
        print(f"Exact Match:{em_cnt/len(df_data) if len(df_data)>0 else 0}")

        with open(os.path.join(self.args.output_dir, f"{self.args.method}.txt"), "w") as f:
            f.write(f"Data Length:{len(df_data)}\n")
            f.write(f"EM counter:{em_cnt}\n")
            f.write(f"Exact Match:{em_cnt/len(df_data) if len(df_data)>0 else 0}\n")

    
    def test_candidates(self, new_col_name="processed_output"):
        df_data = self._get_data(flag='test')
        df_data[new_col_name] = None

        # generate candidates
        candidate_path = os.path.join(self.args.output_dir, f"{self.args.method}_candidate_list.txt")
        candidate_list = []
        with open(candidate_path, "w") as f:
            for index, df_row in tqdm(df_data.iterrows()):
                # gold_query = df_row["tokenized_query"]
                candidates = self.model.generate(self.args, df_row)
                candidate_list.append(candidates)
                for candidate in candidates:
                    f.write(candidate+"\n")
    
        print(f"candidates were saved in {os.path.abspath(candidate_path)} sucessfully!")            

        # test candidates
        em_top1_cnt = 0
        em_topk_cnt = 0
        em_consistency_cnt = 0
        for index, df_row in tqdm(df_data.iterrows()):
            gold_query = df_row["tokenized_query"]
            candidates = candidate_list[index]  # list

            if is_match(candidates[0], gold_query):
                em_top1_cnt += 1
            
            pred_consistency = most_frequent_string(candidates)
            df_data.loc[index, self.col_name] = candidates[0]
            df_data.loc[index, new_col_name] = pred_consistency

            if is_match(pred_consistency ,gold_query):
                em_consistency_cnt += 1

            for candidate in candidates:
                if is_match(candidate, gold_query):
                    em_topk_cnt += 1
                    break
        
        self._save_data(df_data)
        # exact match
        print(f"Data Length:{len(df_data)}")
        print(f"EM@1 counter:{em_top1_cnt}")
        print(f"EM@{self.args.top_k} counter:{em_topk_cnt}")
        print(f"EM_consistency counter:{em_consistency_cnt}")

        print(f"EM@1:{em_top1_cnt/len(df_data) if len(df_data)>0 else 0}")
        print(f"EM@{self.args.top_k}:{em_topk_cnt/len(df_data) if len(df_data)>0 else 0}")
        print(f"EM_consistency:{em_consistency_cnt/len(df_data) if len(df_data)>0 else 0}")

        
        with open(os.path.join(self.args.output_dir, f"{self.args.method}.txt"), "w") as f:
            f.write(f"Data Length:{len(df_data)}\n")
            f.write(f"EM@1 counter:{em_top1_cnt}\n")
            f.write(f"EM@{self.args.top_k} counter:{em_topk_cnt}\n")
            f.write(f"EM_consistency counter:{em_consistency_cnt}\n\n")

            f.write(f"EM@1:{em_top1_cnt/len(df_data) if len(df_data)>0 else 0}\n")
            f.write(f"EM@{self.args.top_k}:{em_topk_cnt/len(df_data) if len(df_data)>0 else 0}\n")
            f.write(f"EM_consistency:{em_consistency_cnt/len(df_data) if len(df_data)>0 else 0}\n")


    