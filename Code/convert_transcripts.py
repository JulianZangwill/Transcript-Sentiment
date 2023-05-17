import re #regular expression (a sequence of characters that forms a search pattern)-> check whether a string matches a regular expression
from io import StringIO  # creates a string buffer (STRING module- in memory-like file like an object)
#Libraries for feature extraction and topic modeling
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer # converts text into a vector of counts, 
# TfidfVectorizer  --> same as CountVectorizer but a bit more advanced (words are assigned a number)
from sklearn.decomposition import LatentDirichletAllocation
#from sklearn.feature_extraction import stop_words
#from sklearn.feature_extraction import _stop_word
#from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stop_words
#Other libraries
import numpy as np
import pandas as pd
import os
import re
import finbert
import lexicon_approach

path = os.getcwd()
files = os.listdir(path +'\Txt_Transcripts')
text_list_dict = {}
for file in files:
    print(f'Cleaning {file} ...')
    f = open('Txt_Transcripts/'+file, 'r').read()
    f = f.replace('!', '. ').replace('? ', '?. ').replace('\n\n', ' ').replace('\n', ' ')
    text_list = f.split('. ')
    text_list = [text for text in text_list if not text.endswith('?')]
    text_list_dict[file] = text_list

print('Done text_list')


#scores = finbert.get_sentiment(text_list_dict)

scores = lexicon_approach.get_sentiment(text_list_dict)


scores_df = pd.DataFrame.from_dict(scores, orient='index').T
scores_summary_df = pd.DataFrame()
scores_summary_df['Labels'] = ['Positive', 'Neutral', 'Negative', 'Total', 'Pos_ratio', 'Neg_ratio', 'Pos_Neg_ratio']

for score in scores:
    list = scores[score]
    pos = 0
    neg = 0
    tot = len(list)
    for x in list:
        if x>0:
            pos+=x
        if x<0:
            neg+=abs(x)
    neut = tot - pos - neg
    print('Positives: ', pos)
    print('Negative: ', neg)
    print('Neutrals: ', neut)
    print('Total Number of sentences: ', tot)

    pos_ratio = pos/tot
    neg_ratio = neg/tot
    pos_neg_ratio = pos/neg
    scores_summary_df[score]  = [pos, neut, neg, tot, pos_ratio, neg_ratio, pos_neg_ratio]


dataframe_path = f'Dataframes\\No_Q_'
scores_df.to_csv(dataframe_path+f'Lexicon_Scores.csv', encoding='utf-8', index=False)
scores_summary_df.to_csv(dataframe_path+'Lexicon_Scores_summary.csv', encoding='utf-8', index=False)
print('Done') 
