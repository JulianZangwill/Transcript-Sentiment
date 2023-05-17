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

###files = ['Standard Chartered PLC.txt']
text_list_dict = {}
result = {}
subdirectory = 'Txt_Transcripts'
for file in files:
    print(f'Cleaning {file} ...')
    f = open(f'{subdirectory}/'+file, 'r').read()
    f = f.replace('!', '. ').replace('? ', '?. ').replace('\n\n', ' ').replace('\n', ' ')
    text_list = f.split('. ')
    text_list = [text for text in text_list if not text.endswith('?')]
    text_list_dict[file] = text_list

print('Done text_list')

lexicon_scores = lexicon_approach.get_sentiment(text_list_dict)
finbert_scores = finbert.get_sentiment(text_list_dict)

total_diffs = 0
total = 0
with open(f'lexicon_difference.txt', 'w') as output:
    for file in files:
        print(file=output)
        print(f'---FILE: {file}', file=output)
        print(file=output)
        text_list = text_list_dict[file]
        diffs = 0
        for i, text in enumerate(text_list):
            l = lexicon_scores[file][i]
            lint = -1 if l < 0 else 1 if l > 0 else 0
            f = finbert_scores[file][i]
            if lint != f:
                diffs += 1
                print(f'  {l:5.2f} {f:2d} {text}', file=output)
        print(file=output)
        print(f'    Differences: {diffs}/{len(text_list)}', file=output)
        print(file=output)
        total_diffs += diffs
        total += len(text_list)

    print(file=output)
    print(f'Total differences: {total_diffs}/{total}', file=output)
    print(file=output)
print('Done') 
