# change the cache dir
# export HF_HOME=./cache/

CUDA_VISIBLE_DEVICES=0 python src/main.py --model_id "meta-llama/Meta-Llama-3-8B-Instruct" --output_dir "output_data/llama3-8B" --method "p_ten_shot" --num_data 1
