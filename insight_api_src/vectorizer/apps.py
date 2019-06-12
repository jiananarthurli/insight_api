from django.apps import AppConfig
import io

class VectorizerConfig(AppConfig):
    name = 'vectorizer'


    def ready(self):

        def load_emb(fname):
            fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
            # n, d = map(int, fin.readline().split())
            data = {}
            for line in fin:
                tokens = line.rstrip().split(' ')
                data[tokens[0]] = list(map(float, tokens[1:]))

            return data

        emb_path = '../insight_api_data/glove.6B.50d.txt'
        # emb_path = '../insight_api_data/wiki-news-300d-1M.vec.txt'

        global emb
        global emb_dim

        emb = load_emb(emb_path)
        emb_dim = 50
        # emb_dim = 300

        print('Embedding loaded.')

