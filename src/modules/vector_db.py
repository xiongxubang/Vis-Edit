import pandas as pd
import numpy as np
from tqdm import tqdm
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document as LangchainDocument


class Retriever:
    def __init__(self, args):
        self.args = args
        print("Load data into Vector DB:")
        self.df_data = pd.read_csv(args.train_data)
        self.data = self._pre_process(self.df_data)

        # Create a dictionary with model configuration options, specifying to use the CPU for computations
        model_kwargs = {'device':'cuda'}
        # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
        encode_kwargs = {'normalize_embeddings': False}
        search_kwargs={"k": args.num_examples}

        # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
        self.embeddings = HuggingFaceEmbeddings(
            model_name=args.embedding_model_id,     # Provide the pre-trained model's path
            model_kwargs=model_kwargs, # Pass the model configuration options
            encode_kwargs=encode_kwargs # Pass the encoding options
        )

        self.db = FAISS.from_documents(self.data, self.embeddings)
        self.retriever = self.db.as_retriever(search_kwargs=search_kwargs)


    def _pre_process(self, df_data:pd.DataFrame):
        return [LangchainDocument(page_content=row["question"], metadata={"question": row["question"], "err_query": row["prediction"], "feedback": row["feedback"], "db_id": row["db_id"], "gt_query":row["tokenized_query"]}) for _, row in tqdm(df_data.iterrows())]
    

    def get_relevant_examples(self, query:str):
        return self.retriever.get_relevant_documents(query)
    
    def get_random_top_k(self):
        num_random_samples = self.args.num_examples
        random_indices = np.random.choice(len(self.data), num_random_samples, replace=False)

        # Retrieve examples
        examples = [self.data[int(i)] for i in random_indices]

        return examples