import pysentiment2 as ps
import os

lm = ps.LM()

def get_sentiment(text_dict):
    print('Getting Sentiment...')
    labels = {0: 0, 1: 1,2: -1}
    sent_val_dict = {}


    for text in text_dict:
        print(f'Sentimenting {text} ...')
        text_list = text_dict[text]
        sent_val = []

        for x in text_list:
            tokens = lm.tokenize(x)
            values = lm.get_score(tokens)
            val = (values['Positive']-values['Negative'])/len(tokens)
            sent_val.append(val)
        sent_val_dict[text] = sent_val
    print('Got Sentiment')
    return sent_val_dict   