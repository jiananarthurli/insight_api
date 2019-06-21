from django.shortcuts import render

from vectorizer.apps import event_list, event_matrix, idf_dict, key_tokens, event_matrix2list_dict, list2event_matrix_dict
from extractor.views import wikiExtractor
from vectorizer.views import tf_idf

from django.http import HttpResponse
import json
import numpy as np

from time import time

# Create your views here.


def predict(event_matrix, vec_norm, threshold):

    prod = vec_norm.dot(event_matrix.T)
    # returned values are the indices of the SELECTED events, or the event matrix indices
    event_pred = list(np.nonzero(prod[0, :] > threshold)[0])

    return event_pred


def recommender(request):

    threshold = 0.235

    wiki_topic = request.GET['wiki_topic']
    wiki_text = wikiExtractor(wiki_topic)

    tic = time()

    wiki_vec = tf_idf(wiki_text, key_tokens, idf_dict)

    recommendations = predict(event_matrix, wiki_vec.reshape(1, -1), threshold)

    found = False
    recommendation_list = []

    if len(recommendations) != 0:
        found = True
        for ix in recommendations:
            event_ix = int(event_matrix2list_dict[str(ix)])
            recommendation_list.append(event_list[event_ix])

    response_dict = {
        'found' : found,
        'events' : recommendation_list # top 3
    }

    response = json.dumps(response_dict)

    print("Time lapse {}".format(time() - tic))

    return HttpResponse(response)
