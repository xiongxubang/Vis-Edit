# https://huggingface.co/learn/cookbook/rag_evaluation
# https://medium.com/@akriti.upadhyay/implementing-rag-with-langchain-and-hugging-face-28e3ea66c5f7
import argparse
import os
import pandas as pd
from tqdm import tqdm

from experiments.llm_exp import LLMExp

def get_parser():
    parser = argparse.ArgumentParser(description="llm config")
    parser.add_argument(
        "--train_data",
        type=str,
        default="input_data/NVBench-Feedback/cross-domain/train.csv",
        help="the path of train_data (csv)",
    )
    parser.add_argument(
        "--dev_data",
        type=str,
        default="input_data/NVBench-Feedback/cross-domain/dev.csv",
        help="the path of dev_data (csv)",
    )
    parser.add_argument(
        "--test_data",
        type=str,
        default="input_data/NVBench-Feedback/cross-domain/test.csv",
        help="the path of test_data (csv)",
    )
    parser.add_argument(
        "--db_path",
        type=str,
        default="input_data/NVBench-Feedback/database/",
        help="the path of the database dir",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="output_data/",
        help="the path of output_dir",
    )
    parser.add_argument(
        "--method",
        type=str,
        default="zero_shot",
        help="the name of the used method",
    )
    parser.add_argument(
        "--model_id",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",      # /project/kdd/xxiongag/project/models/Meta-Llama-3-70B-Instruct
        help="the path of model",
    )
    parser.add_argument(
        "--embedding_model_id",
        type=str,
        default="sentence-transformers/all-MiniLM-l6-v2",      
        help="the path of embedding model",
    )
    parser.add_argument(
        "--num_examples",
        type=int,
        default=10,
        help="the number of examples used in the in-context learning",
    )
    parser.add_argument(
        "--num_data",
        type=int,
        default=None,
        help="the number of test data",
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=10,
        help="the number of generated candidate clauses",
    )
    parser.add_argument(
        '--test_candidates',
        action='store_true', 
        default=False,
        help="whether to generate and test candidates and store them in txt file",
    )

    args = parser.parse_args()

    return args

    

if __name__ == "__main__":
    args = get_parser()

    print("current pid: ",os.getpid())
    print("parent pid: ",os.getppid())

    experiment = LLMExp(args)
    if args.test_candidates:
        experiment.test_candidates()
    else:
        experiment.test()