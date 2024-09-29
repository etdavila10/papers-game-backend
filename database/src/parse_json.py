import json
import random

wanted_keys = ('id', 'categories')

cats_dict = {}

print('Starting to process the json file')

with open('data/raw_data.json', 'r') as f:
    for data_obj in f:
        data_dict = json.loads(data_obj)
        # if random.random() < .0005:
        # filter to desired keys
        processed_dict = dict((k, data_dict[k]) for k in wanted_keys)

        # create array for categories
        processed_dict['categories'] = processed_dict['categories'].split(' ')

        for cat in processed_dict['categories']:
            if cat not in cats_dict:
                cats_dict[cat] = []
            cats_dict[cat].append(processed_dict['id'])

with open('data/processed_data.json', 'w') as output_file:
    json.dump(cats_dict, output_file)

print('Output file created with wanted keys')
