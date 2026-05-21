#!/bin/bash

# 参数定义
model_name=Autoformer
train_epochs=10
learning_rate=0.01
llama_layers=32
llm_dim=768

batch_size=24
d_model=32
d_ff=128

comment='security-test1'

# 启动命令
python -m torch.distributed.run --rdzv_endpoint=localhost:9999 run_main.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/security/ \
  --data_path data_v2.csv \
  --model_id security \
  --model $model_name \
  --data security \
  --features M \
  --seq_len 32 \
  --label_len 4 \
  --pred_len 16 \
  --factor 3 \
  --enc_in 200 \
  --dec_in 200 \
  --c_out 200 \
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
  --use_amp
