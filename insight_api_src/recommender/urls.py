from django.conf.urls import url
from recommender.views import recommender


urlpatterns = [
    url('', recommender, name='submission'),
]


