# Interactive Text-to-Visualization: Refining Visualization Outputs Through Natural Language User Feedback

## Setup

Step 1. Download the dataset from [Google Drive](https://drive.google.com/drive/folders/1yXnZR0BnGXHOYU9aVtXMtXz0heUBfZBz?usp=sharing)

Step 2. Extract `NVBench-Feedback.zip` to `Vis-Edit/input_data/`

The project structure should look like this:
```
Vis-Edit/
├── input_data/
│   └── NVBench-Feedback/
├── output_data/
├── scripts/
├── src/
├── readme.md
└── Technical_Report.pdf
```

The contents of each directory are as follows:
- `input_data/`: Contains the NVBench-Feedback dataset
- `output_data/`: Stores refined queries and prompt strategy results
- `scripts/`: Contains demo run scripts
- `src/`: Source code including baselines, ablation studies, and parameter studies

For detailed information, refer to our [`technical report`](./Technical_Report.pdf).

## Requirements

- Python 3.8
- PyTorch 2.2.0
- CUDA 11.8
- Transformers 4.41.2

Example command to install dependencies (as listed in `src/requirement.txt`):
```bash
!pip install -q torch transformers transformers langchain sentence-transformers tqdm pandas datasets langchain-community
```

## Usage

Run from the `Vis-Edit` directory:

```bash
# For EM@1 evaluation only
./scripts/run.sh

# For both EM@1 and EM@10 evaluation + top-10 query candidates
./scripts/run_with_candidates.sh
```

### Parameters

- `model_id`: HuggingFace model path
- `output_dir`: Results save location
- `num_data`: Number of test items to evaluate (in order)
- `method`: Strategy name (defined in `src/experiments/llm_exp.py:50`)
- `test_candidates`: Enable top-10 query candidate generation (only for methods with "candidate" suffix)



