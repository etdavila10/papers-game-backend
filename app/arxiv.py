import requests
import xmltodict
import json

base_url = 'https://export.arxiv.org/api/query?id_list='

def call_arxiv_api(paper_ids):
    full_url = base_url + ','.join(paper_ids)
    response = requests.get(full_url)

    data_dict = xmltodict.parse(response.content)

    return data_dict
