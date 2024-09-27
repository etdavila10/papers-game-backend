import json
import random
import sys
from pathlib import Path

Path("data/categories").mkdir(parents=True, exist_ok=True)

output_file = open('data/mapped_data.json', 'w')

cats_dict = {}

percent_keep = .00005

with open('data/processed_data.json', 'r') as f:
    data_list = json.load(f)
    for data_obj in data_list:
        if random.random() < percent_keep:
            for cat in data_obj['categories']:
                if cat not in cats_dict:
                    cats_dict[cat] = []
                cats_dict[cat].append(data_obj['id'])

size = 0
for key in cats_dict:
    size += sys.getsizeof(cats_dict[key])

print("total memory used in bytes: " + str(size))

with open('data/remapped_data.json', 'w') as mapped_file:
    json.dump(cats_dict, mapped_file)

print('Mapped data file created')

