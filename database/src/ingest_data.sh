#!/bin/bash

# Get the updated data from kaggle This will download a zip file
kaggle datasets download Cornell-University/arxiv

echo 'Extracting "arxiv.zip" into data/'
unzip -o arxiv -d data

echo 'Changing downloaded json file name to "raw_data.json"'
mv data/arxiv-metadata-oai-snapshot.json data/raw_data.json

echo 'Removing "arxiv.zip"'
rm arxiv.zip

# start the parse_json.py script
# This will process the data and should
# create a 'processed_data.json' in data
# directory
python parse_json.py

# run the 'schema.py' script
# this will create the tables necessary
# to load in the updated data

# run a 'load_data.py' script
# which will go through and load the
# processed_data.json file into the
# database tables
