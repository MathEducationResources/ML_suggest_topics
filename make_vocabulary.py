import os
import glob
import json
import re
from nltk import PorterStemmer
from nltk.corpus import stopwords
from helpers import find_math_words


def strip_text(text):

    math_words = find_math_words(text)

    text = text.replace('<span class=\"math\">', 'code_word_begin')
    text = text.replace('</span>', 'code_word_end')
    text = re.sub(r'(?<=code_word_begin)(.*?)(?=code_word_end)', ' ', text,
                  flags=re.DOTALL)

    text = text.replace('<em>', 'code_word_begin')
    text = text.replace('</em>', 'code_word_end')
    text = re.sub(r'(?<=code_word_begin)(.*?)(?=code_word_end)', ' ', text,
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

    return list_voc + math_words


if __name__ == '__main__':

    vocabulary = []
    topic_list = []

    fo_list = [x[0] for x in os.walk('../json_data')]
    for folder in fo_list:
        fofo_list = [x[0] for x in os.walk(folder)]
        for fofolder in fofo_list:
            Files = glob.glob(fofolder + '/*.json')
            for File in Files:
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

                list_voc = strip_text(text)
                stop = stopwords.words('english')

                for voc in list_voc:
                    voc = str(voc)
                    voc = PorterStemmer().stem_word(voc)
                    if voc not in stop and voc not in vocabulary:
                        vocabulary.append(voc)

                if 'topics' in data:
                    topics = data['topics']
                    for topic in topics:
                        topic = str(topic)
                        if topic not in topic_list:
                            topic_list.append(topic)

    f = open('vocabulary.csv', 'w')
    f.write('Number,Voc\n')
    for zahl in range(len(vocabulary)):
        f.write('%i,%s\n' % (zahl, vocabulary[zahl]))
    f.close()

    f = open('topics.csv', 'w')
    f.write('Number,Topic\n')
    for zahl in range(len(topic_list)):
        f.write('%i,%s\n' % (zahl, topic_list[zahl]))
    f.close()
