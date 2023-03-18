#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:27:23 2020

@author: ngatran
"""

import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import collections
import nltk.downloader
nltk.download('words')
nltk.download('omw-1.4')
words = set(nltk.corpus.words.words())
lemmatizer = WordNetLemmatizer()
filepath_cmw = "./common_words.xlsx"


#Source: https://towardsdatascience.com/cleaning-text-data-with-python-b69b47b97b76
def remove_useless_characters(text):   
    useless_1 = ["’s", "n’t", "’re", "’m", "’ll", "\xa0", "\n"
                ,"’ve", "’d", "…", "Y’","'s", "n't", "'d", "'ve", "'ll", "'re", "s'", "'m"]
    useless_2 = ['‘', '.', ',', ';', '-', '?', '!', '*', ':', '''"''', '(', ')', ']'
                , '[','...', "’", "—", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "%",'”', '“', "'", "$", '”']
    for x in useless_1:
        text = text.replace(x,' ')
    for x in useless_2:
        text = text.replace(x,' ')
    return(text)
    
def remove_common_words(word_list):
    df_common = pd.read_excel(filepath_cmw, sheet_name = 'Main')
    common_words = list(df_common.Words)
    word_list = [x for x in word_list if x not in common_words]
    word_list = [lemmatizer.lemmatize(x, wordnet.VERB) for x in word_list]
    word_list = [x for x in word_list if x not in common_words]
    word_list = [lemmatizer.lemmatize(x, wordnet.NOUN) for x in word_list]
    word_list = [x for x in word_list if x not in common_words]    
    word_list = list(dict.fromkeys(word_list))
    return(word_list)

def remove_meaningless_words(word_list):
    word_list = [w for w in word_list if w in words or not w.isalpha()]
    return(word_list)


