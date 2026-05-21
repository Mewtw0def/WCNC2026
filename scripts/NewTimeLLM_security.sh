#!/bin/bash

# 参数定义
model_name=NewTimeLLM
train_epochs=10
learning_rate=0.01
llama_layers=32
#llm_dim=768
llm_dim=4096
llm_model='LLAMA'

batch_size=12
d_model=32
d_ff=128

num_process=1
master_port=10008
comment='security-new-test1'

# 启动命令
python -m torch.distributed.run --rdzv_endpoint=localhost:10009 run_new.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/security/ \
  --data_path data_v4.csv \
  --model_id security_new_llama_512_336 \
  --model $model_name \
  --data security_new \
  --features M \
  --seq_len 512 \
  --label_len 4 \
  --pred_len 336 \
  --factor 3 \
  --enc_in 50 \
  --dec_in 50 \
  --c_out 50 \
  --des 'Exp' \
  --itr 1 \
  --d_model $d_model \
  --d_ff $d_ff \
  --batch_size $batch_size \
  --learning_rate $learning_rate \
  --llm_layers $llama_layers \
  --llm_dim $llm_dim \
  --train_epochs $train_epochs \
  --model_comment $comment \
  --n_heads 32 \
  --llm_model $llm_model
