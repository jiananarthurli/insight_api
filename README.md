# insight_api

This is the Django API server source codes for the the Insight Data Science Project Weekendpedia (https://chrome.google.com/webstore/search/weekendpedia). 

**Weekendpedia** is an Chrome extension that recommend cultural events (in galleries, museums, etc) in New York City for Wikipedia users. The extension will track the current Wikipedia topic that the user is viewing, and alert the user when a relevant cultural event is found. Ths repo contains the Django backend for the API server (in ```./insight_api_src```), and a notebook that explains how the recommender works (in ```./recommender_prototype```). The event data is scraped from nyc.com (stored in ```./insight_api_data```).

![API service](./Images/FrontEndBackEnd.png "Weekendpedia")

The Django API server has three components: extractor, vectorizer and recommender. 

The extractor (```./insight_api_src/extractor/```) retrieves pure texts of the Wikipedia topic that the user is viewing, using the API provided by Wikipedia. The functions are defined in ```./insight_api_src/extractor/views.py```.

