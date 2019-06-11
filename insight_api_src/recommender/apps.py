from django.apps import AppConfig
import json

class RecommenderConfig(AppConfig):
    name = 'recommender'

    def ready(self):

        global events_list

        events_list = []

        with open('../insight_api_data/event_list.txt', 'r') as f:
            events_list = json.load(f)