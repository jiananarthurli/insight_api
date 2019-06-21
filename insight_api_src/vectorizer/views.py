from django.shortcuts import render
import numpy as np
from vectorizer.apps import emb, emb_dim

# Create your views here.

#
# def article2Vec(text):
#
#     words = text.strip().replace('.', '').replace(',', '').lower().split(' ')
#     vec = np.zeros((emb_dim,))
#     counter = 0
#     for word in words:
#         try:
#             vec += np.array(emb[word])
#             counter += 1
#         except KeyError:
#             continue
#     # averaging and summing would have different biases
#     vec /= counter
#
#     return vec


def preprocess(text):
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


def doc2tag(text):
    sentences = nltk.sent_tokenize(text)
    noun_list = []
    for s in sentences:
        tokens = nltk.word_tokenize(s)
        text_tagged = nltk.pos_tag(tokens)
        pair = [(word, pos) for (word, pos) in text_tagged]
        noun_list.extend(pair)

    return noun_list


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
