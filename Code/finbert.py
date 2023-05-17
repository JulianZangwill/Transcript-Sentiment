import transformers
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
import pandas as pd
import torch


def get_sentiment(text_dict):
    print('Getting Sentiment...')
    finbert_pretrained = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
    labels = {0: 0, 1: 1,2: -1}
    sent_val_dict = {}

    for text in text_dict:
        print(f'Sentimenting {text} ...')
        text_list = text_dict[text]
        sent_val = []

        for x in text_list:
            inputs = tokenizer(x, return_tensors="pt", padding=True) # convert the sentence into vectors, padding true as two sentences may not have the same length
            outputs = finbert_pretrained(**inputs)[0]
    
            val = labels[np.argmax(outputs.detach().numpy())]
            sent_val.append(val)
        sent_val_dict[text] = sent_val
    print('Got Sentiment')
    return sent_val_dict   