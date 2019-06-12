from django.shortcuts import render
import numpy as np
from vectorizer.apps import emb, emb_dim

# Create your views here.


def article2Vec(text):

    words = text.strip().replace('.', '').replace(',', '').lower().split(' ')
    vec = np.zeros((emb_dim,))
    counter = 0
    for word in words:
        try:
            vec += np.array(emb[word])
            counter += 1
        except KeyError:
            continue
    # averaging and summing would have different biases
    vec /= counter

    return vec
