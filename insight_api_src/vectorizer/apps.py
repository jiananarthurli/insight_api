from django.apps import AppConfig
import json
import numpy as np

class VectorizerConfig(AppConfig):
    name = 'vectorizer'

    def ready(self):

        global event_matrix
        global idf_dict
        global key_tokens
        global event_matrix2list_dict
        global list2event_matrix_dict

        data_dir = '../insight_api_data/'
        event_matrix_path = data_dir + 'event_matrix.csv'
        idf_dict_path = data_dir + 'idf_dict.json'
        key_tokens_path = data_dir + 'key_tokens.json'
        event_matrix2list_dict_path = data_dir + 'event_matrix2list_dict.json'
        list2event_matrix_dict_path = data_dir + 'list2event_matrix_dict.json'

        with open(event_matrix_path, 'r') as f:
            event_matrix = np.genfromtxt(f, delimiter=',')
        with open(idf_dict_path, 'r') as f:
            idf_dict = json.load(f)
        with open(key_tokens_path, 'r') as f:
            key_tokens = json.load(f)
        with open(event_matrix2list_dict_path, 'r') as f:
            event_matrix2list_dict = json.load(f)
        with open(list2event_matrix_dict_path, 'r') as f:
            list2event_matrix_dict = json.load(f)

        print('Data loaded.')






