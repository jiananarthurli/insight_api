from django.shortcuts import render

import re
import nltk
import spacy
import numpy as np

from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")
stop = set(stopwords.words('english'))
stop_words = set(['event', 'collection', 'street', 'many',
                  'exhibition', 'work', 'monday', 'tuesday',
                  'wednesday', 'thursday', 'friday', 'saturday',
                  'sunday', 'new', 'york', 'new york', 'new york city',
                  'visit', 'museum', 'world', 'department', 'NYC'
                 ])
stop.update(stop_words)

def preprocess(text):

    # text cleaning
    text = text.replace('\n', ' ')
    text = text.replace('&#x27;', "'")
    text = text.replace('&#x2019;', "'")
    text = text.replace('B.C.', "BC")
    text = text.replace('A.D.', "AD")
    text = text.replace('&amp;', "and")

    # remove ',' in numbers
    text = re.sub('(\d+),(\d+)', lambda x: "{}{}".format(x.group(1).replace(',', ''), x.group(2)), text)
    text = re.sub('&#x(.*?);', ' ', text)
    text = re.sub('http(.+?) ', '', text)

    return text

# PoS tagging for text
def doc2tag(text):

    sentences = nltk.sent_tokenize(text)
    tag_list = []
    for s in sentences:
        tokens = nltk.word_tokenize(s)
        text_tagged = nltk.pos_tag(tokens)
        pair = [(word, pos) for (word, pos) in text_tagged]
        tag_list.extend(pair)

    return tag_list


# find PoS pattern of NNP, NNP, NN
def nnp_nn(text):

    patterns = "NNP_NN: {<NNP>+(<NNS>|<NN>+)}"  # at least one NNP followed by NNS or at least one NN
    parser = nltk.RegexpParser(patterns)
    p = parser.parse(doc2tag(text))
    phrase = []
    for node in p:
        if type(node) is nltk.Tree:
            phrase_str = ''
            for w in node:
                phrase_str += w[0]
                phrase_str += ' '
            phrase_str = phrase_str.strip()
            phrase.append(phrase_str)
    return phrase


# find PoS pattern of JJ, NN
def jj_nn(text):

    patterns = "NNP_NN: {<JJ>+(<NN>+)}"  #
    parser = nltk.RegexpParser(patterns)
    p = parser.parse(doc2tag(text))
    phrase = []
    for node in p:
        if type(node) is nltk.Tree:
            phrase_str = ''
            for w in node:
                phrase_str += w[0]
                phrase_str += ' '
            phrase_str = phrase_str.strip()
            phrase.append(phrase_str)
    return phrase


# calculate TF-IDF vector for the text, assume trigrams
def tf_idf(text, key_tokens, idf_dict, ngram=3):

    tf_idf_dict = defaultdict(int)

    text = text.lower()

    # tokens been used for tf-idf
    tokens = nltk.word_tokenize(text)

    # get unigram, bigram, trigram
    token_list = []
    for i in range(1, ngram + 1):
        token_list.extend(nltk.ngrams(tokens, i))
    token_list = [' '.join(token) for token in token_list]

    # lemmatize the tokens
    for i, token in enumerate(token_list):
        token_list[i] = lemmatizer.lemmatize(token)

    # initialize the tf_idf_dict with all the tokens to be used
    for token in key_tokens:
        tf_idf_dict[token] = 0

    # count frequency of each token
    for token in token_list:
        if token in key_tokens:
            tf_idf_dict[token] += 1

    # tf-idf vector calculation
    for key in tf_idf_dict.keys():
        tf_idf_dict[key] = tf_idf_dict[key] * idf_dict[key]

    tf_idf_vec = np.zeros((len(key_tokens),))
    for i, key in enumerate(key_tokens):
        tf_idf_vec[i] = tf_idf_dict[key]

    # returns a normalized 1d np array
    tf_idf_vec = tf_idf_vec / np.linalg.norm(tf_idf_vec)

    return tf_idf_vec


