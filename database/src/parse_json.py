import json

wanted_keys = ('id', 'categories')

data_array = []

with open('data/raw_data.json', 'r') as f:
    for data_obj in f:
        data_dict = json.loads(data_obj)
        # filter to desired keys
        processed_dict = dict((k, data_dict[k]) for k in wanted_keys)

        # create array for categories
        processed_dict['categories'] = processed_dict['categories'].split(' ')

        # write to processed json file
        data_array.append(processed_dict)

with open('data/processed_data.json', 'w') as output_file:
    json.dump(data_array, output_file)

print('Output file created with wanted keys')

