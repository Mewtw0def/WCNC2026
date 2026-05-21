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

        #self.lstm = nn.LSTM(input_size=configs.enc_in, hidden_size=configs.d_model, batch_first=True)
        self.lstm = nn.LSTM(input_size=1, hidden_size=configs.d_model, batch_first=True)
        self.projection = nn.Linear(configs.d_model, configs.c_out)

        if self.task_name == 'classification':
            self.dropout = nn.Dropout(configs.dropout)
            self.flatten = nn.Flatten()
            self.classifier = nn.Linear(configs.d_model * self.seq_len, configs.num_class)

    def encoder(self, x):
        out, _ = self.lstm(x)
        return self.projection(out)

    def forecast(self, x_enc):
        return self.encoder(x_enc)[:, -self.pred_len:, :]

    def imputation(self, x_enc):
        return self.encoder(x_enc)

    def anomaly_detection(self, x_enc):
        return self.encoder(x_enc)

    def classification(self, x_enc):
        x = self.encoder(x_enc)
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

