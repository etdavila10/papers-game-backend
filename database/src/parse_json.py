import json
from datetime import datetime

wanted_keys = ('id', 'authors', 'title', 'categories', 'abstract', 'versions')
date_format = '%a, %d %b %Y %H:%M:%S %Z'

output_file = open('data/processed_data.json', 'w')

def versions_to_timestamp(versions):
    for version_dict in versions:
        if version_dict['version'] == 'v1':
            date_str = version_dict['created']
            dt_obj = datetime.strptime(date_str, date_format)
            return dt_obj.timestamp()
    return


with open('data/raw_data.json', 'r') as f:
    for data_obj in f:
        data_dict = json.loads(data_obj)
        # filter to desired keys
        processed_dict = dict((k, data_dict[k]) for k in wanted_keys)

        # convert versions list to one timestamp corresponding to initial
        # upload date
        processed_dict['timestamp'] = versions_to_timestamp(processed_dict['versions'])
        # delete versions key
        processed_dict.pop('versions', None)

        # write to processed json file
        processed_json = json.dumps(processed_dict) + '\n'
        output_file.write(processed_json)

output_file.close()
print('Output file created with wanted keys')

