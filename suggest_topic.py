import os
import glob
import json
import re
import pandas as pd
import sys
import numpy as np
from nltk import PorterStemmer
import scipy
import pickle
import sklearn


def strip_text(text):

    text = text.replace('<span class=\"math\">', 'code_word_begin')
    text = text.replace('</span>', 'code_word_end')
    text = re.sub(
        r'(?<=code_word_begin)(.*?)(?=code_word_end)', ' ', text, flags=re.DOTALL)

    text = text.replace('<em>', 'code_word_begin')
    text = text.replace('</em>', 'code_word_end')
    text = re.sub(
        r'(?<=code_word_begin)(.*?)(?=code_word_end)', ' ', text, flags=re.DOTALL)

    text.strip()

    text = text.lower()
    text = text.replace('<p>', ' ')
    text = text.replace('</p>', ' ')
    text = text.replace('code_word_begin', ' ')
    text = text.replace('code_word_end', ' ')
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace(';', ' ')
    text = text.replace('?', ' ')
    text = text.replace('!', ' ')
    text = text.replace('\n', '')
    text = re.sub(r'[^a-z ]', ' ', text)

    list_voc = re.split(r'[ ]+', text)

    return list_voc


if __name__ == '__main__':

    df_vocabulary = pd.read_csv('vocabulary.csv')
    vocs = list(df_vocabulary['Voc'])
    df_topics = pd.read_csv('topics.csv')
    topic_list = list(df_topics['Topic'])
    clf = pickle.load(open("classifier.bin", "rb"))

    fo_list = [x[0] for x in os.walk('../json_data')]
    for folder in fo_list:
        Files = glob.glob(folder + '/*.json')
        for File in Files:

            x_vec = np.zeros(shape=(1, len(vocs)))

            fd = open(File, 'r')
            data = json.loads(fd.read())
            fd.close()
            
            text = ''
            statement_html = data['statement_html']
            text = text + statement_html + ' '
            hints_html = data['hints_html']
            for hint in hints_html:
                text = text + hint + ' '
            sols_html = data['sols_html']
            for sol in sols_html:
                text = text + sol + ' '
            list_words = strip_text(text)

            for word in list_words:
                word = str(word)
                voc = PorterStemmer().stem_word(word)
                if word in vocs:
                    x_vec[0][vocs.index(word)] = 1

            y_vec = clf.predict_proba(x_vec)[0]
            index1 = y_vec.argmax()
            y_vec[index1] = 0
            index2 = y_vec.argmax()
            
            if 'topics' in data:
                given_topics = data['topics']
            else:
                given_topics = []
                
            suggested_topics = []
            if topic_list[index1] not in given_topics:
                suggested_topics.append(topic_list[index1])
            if index2 > 0.5 and topic_list[index2] not in given_topics:
                suggested_topics.append(topic_list[index2])
      
            data['topic_suggest'] = suggested_topics

            with open(File, "w") as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
