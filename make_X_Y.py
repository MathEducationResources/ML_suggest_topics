import os
import glob
import json
import re
import pandas as pd
import numpy as np
from nltk import PorterStemmer
import scipy


def strip_text(text):

    text = text.replace('<span class=\"math\">', 'code_word_begin')
    text = text.replace('</span>', 'code_word_end')
    text = re.sub(
        r'(?<=code_word_begin)(.*?)(?=code_word_end)', ' ', text,
        flags=re.DOTALL)

    text = text.replace('<em>', 'code_word_begin')
    text = text.replace('</em>', 'code_word_end')
    text = re.sub(
        r'(?<=code_word_begin)(.*?)(?=code_word_end)', ' ', text,
        flags=re.DOTALL)

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

    X = np.zeros(shape=(1, len(vocs)))
    Y = np.zeros(shape=(1, len(topic_list)))

    fo_list = [x[0] for x in os.walk('../json_data')]
    for folder in fo_list:
        Files = glob.glob(folder + '/*.json')
        for File in Files:

            x_vec = np.zeros(shape=(1, len(vocs)))
            y_vec = np.zeros(shape=(1, len(topic_list)))

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

            if 'topics' in data:
                topics = data['topics']
                for topic in topics:
                    topic = str(topic)
                    y_vec[0][topic_list.index(topic)] = 1

            for word in list_words:
                word = str(word)
                voc = PorterStemmer().stem_word(word)
                if word in vocs:
                    x_vec[0][vocs.index(word)] = 1
            if 1 in y_vec:
                X = np.append(X, x_vec, 0)
                Y = np.append(Y, y_vec, 0)

    X = scipy.delete(X, 0, 0)
    Y = scipy.delete(Y, 0, 0)

    np.savetxt('X_data.csv', X, delimiter=",", fmt='%.1d')
    np.savetxt('Y_data.csv', Y, delimiter=",", fmt='%.1d')
