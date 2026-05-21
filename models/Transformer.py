import torch
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self, configs):
        super(Model, self).__init__()
        torch.backends.cudnn.enabled = False
        self.task_name = configs.task_name
        self.seq_len = configs.seq_len
        self.pred_len = configs.seq_len if self.task_name in ['classification', 'anomaly_detection', 'imputation'] else configs.pred_len

        self.embedding = nn.Linear(1, configs.d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=configs.d_model, nhead=configs.n_heads, dim_feedforward=configs.d_ff, dropout=configs.dropout)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=configs.e_layers)
        self.projection = nn.Linear(configs.d_model, configs.c_out)

        if self.task_name == 'classification':
            self.flatten = nn.Flatten()
            self.dropout = nn.Dropout(configs.dropout)
            self.classifier = nn.Linear(configs.d_model * self.seq_len, configs.num_class)

    def forward_transformer(self, x):
        x = self.embedding(x)
        x = x.permute(1, 0, 2)  # (S, B, E)
        x = self.encoder(x)
        x = x.permute(1, 0, 2)  # (B, S, E)
        return self.projection(x)

    def forecast(self, x_enc):
        return self.forward_transformer(x_enc)[:, -self.pred_len:, :]

    def imputation(self, x_enc):
        return self.forward_transformer(x_enc)

    def anomaly_detection(self, x_enc):
        return self.forward_transformer(x_enc)

    def classification(self, x_enc):
        x = self.forward_transformer(x_enc)
        x = self.flatten(x)
        return self.classifier(self.dropout(x))

    def forward(self, x_enc, x_mark_enc, x_dec, x_mark_dec, mask=None):
        if self.task_name in ['long_term_forecast', 'short_term_forecast']:
            return self.forecast(x_enc)
        elif self.task_name == 'imputation':
            return self.imputation(x_enc)
        elif self.task_name == 'anomaly_detection':
            return self.anomaly_detection(x_enc)
        elif self.task_name == 'classification':
            return self.classification(x_enc)
        else:
            return None

