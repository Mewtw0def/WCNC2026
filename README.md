## Fusing Situations of Massive Mobile Nodes Improves the LLM-Based Attack Prediction for AI-Native Edges（WCNC2026）

This project implemented a time series prediction method based on LLM to predict the development of attacks.

### Data Generation

Generate datasets with different experimental parameters by modifying the parameters in generation/main.py and running it.

```python
num_nodes = 100
prob_edge = 0.1
tot = 20000 * 50 * 2
beta = 0.1
gamma = 0.05
```

### Experimental operation

Adjust the contents of each. sh file ending in **security** in the scripts folder according to the required data.
Taking NewTimeLLM (the method proposed in this article) as an example

```sh
#!/bin/bash


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
```

During the experiment, the long-term prediction experiment seq_len was 512 and pred_len was 336, while the short-term prediction experiment seq_len was 96 and pred_len was 96. Adjustments were made according to different types of experiments. For model comparison, switch the llm_model parameter between 'LLAMA' and 'GPT-2'. Depending on the model method to be used, switch to running the sh file ending in security to generate data content.
