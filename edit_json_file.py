import json
import random

with open("london_p.json", 'r') as f: #london_p_footfall_sales.json
    data = json.load(f)

data_type = data["features"]

for item in data_type:
    item["properties"]["footfall"] = (random.randint(1,1000))
    item["properties"]["sales"] = (random.randint(1, 1000))

with open('new_london_p.json', 'w') as json_file:
    json.dump(data_type, json_file)

# after you need to add extra meta json to make it work.