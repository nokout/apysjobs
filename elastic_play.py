from elasticsearch import Elasticsearch
import json


es = Elasticsearch()

with open('output/10698254.json') as f:
    notice = json.load(f)


    es.index(index='notices',
              doc_type='notice',
              body=notice,
              id = notice['id'])

print(json.dumps(es.count('notices'), indent=4))
print(json.dumps(es.indices.stats('notices', fields='id'), indent=4))
