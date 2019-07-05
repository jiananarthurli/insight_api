import pandas as pd
import json
from sqlalchemy import create_engine

path = '/home/arthurli/insight_api/insight_api_data'
filename = 'event_list.txt'

with open(path + filename, 'r') as f:
    event_list_json = json.load(f)

event_list = pd.DataFrame(event_list_json)

engine = create_engine('postgresql://arthurli:chrome_insight@localhost:5432/insight', echo=False)
event_list.to_sql(con=engine, name='event_list', if_exists='replace', chunksize=1000)