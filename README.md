# insight_api

This is the Django API server source codes for the the Insight Data Science Project Weekendpedia (https://chrome.google.com/webstore/search/weekendpedia). 

**Weekendpedia** is an Chrome extension that recommend cultural events (in galleries, museums, etc) in New York City for Wikipedia users. The extension will track the current Wikipedia topic that the user is viewing, and alert the user when a relevant cultural event is found. This repo contains the Django backend for the API server (in ```./insight_api_src```), and a notebook that explains how the recommender works (in ```./recommender_prototype```). The event data is scraped from *nyc.com* (stored in ```./insight_api_data```).

![API service](./Images/FrontEndBackEnd.png "Weekendpedia")

The Django API server has three components: extractor, vectorizer and recommender. 

The extractor (```./insight_api_src/extractor/```) retrieves pure texts of the Wikipedia topic that the user is viewing, using the API provided by Wikipedia. The functions are defined in ```./insight_api_src/extractor/views.py```.

The source codes for the Chrome extension is in another repo <https://github.com/jiananarthurli/insight_chrome_extension.git>. 

The vectorizer (```./insight_api_src/vectorizer/```) converts the text into a feature vector using TF-IDF algorithm (details are explained in the notebook in ```./recommender_prototype```), and sent to the recommender.

The recommender (```./insight_api_src/vectorizer/```) calculates the cosine similarities between the feature vectors of the wiki texts and the pre-calcualted feature vectors of the events. Events are recommended when the similarities are higher than the threshold. The event infomation (name, description, link, etc) is retrieved from the PostgreSQL server and returned as JSON strings. 
