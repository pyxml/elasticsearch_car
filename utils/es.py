import json

from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()


def create_es():
	body = {
		"mappings": {
			"doc": {
				"properties": {
					"title": {
						"type": "text",
						"analyzer": "ik_max_word"
					},
					"a_url": {
						"type": "text"
					},
					"summery": {
						"type": "text"
					},
					"action_type": {
						"type": "text"
					},
					"a_uuid": {
						"type": "text"
					}
				}
			}
		}
	}
	es.indices.create(index="sf ", body=body)


def filter_es(action_type, search_msg):
	body = {
		"from":0,
		"size": es.count(index="sf")["count"],
		"query": {
			"bool": {
				"must": [
					{"match": {
						"title": search_msg
					}},
					{
						"match": {
							"action_type": action_type
						}
					}
				]
			}
		},
		"highlight": {
			"pre_tags": "<b style='color: red;font-size:16px'>",
			"post_tags": "</b>",
			"fields": {"title": {}}
		}
	}

	return es.search(index="sf", body=body, filter_path=["hits.total", "hits.hits"])


def add_es(title, a_url, summery, action_type, a_uuid):
	body = {
		"title": title,
		"a_url": a_url,
		"summery": summery,
		"action_type": action_type,
		"a_uuid": a_uuid
	}
	es.index(index="sf", doc_type="doc", body=body)


def index_msg():
	import os

	abs_path = os.path.abspath(__file__)
	utils_path = os.path.dirname(abs_path)
	data_path = os.path.join(utils_path, "data")

	for i in os.listdir(data_path):
		file_path = os.path.join(data_path, i)
		s = set()

		with open(file_path, "r", encoding="utf8")as f:
			for line in f:
				data_msg = json.loads(line)["content"]
				t = es.indices.analyze(body={'analyzer': "ik_max_word", "text": data_msg})["tokens"]
				st = {i["token"] for i in t}
				s.update(st)
	f = open("a.txt", "w", encoding="utf8")
	json.dump(" ".join(s), f)
	f.flush()
	f.close()


def load_msg():
	with open('a.txt', "r")as f:
		res = json.load(f).split(" ")
		print(len(res))


# action=[{
# 	"_index":"q1",
# 	"_type":"doc",
# 	"_source":{
# 		"title":i
# 	}
# } for i in res]
# print(helpers.bulk(es,action))

def suggest_es(search_msg):
	body2 = {
		"suggest": {
			"q1": {
				"text": search_msg,
				"completion": {
					"field": "title"
				}
			}
		}
	}
	return es.search(index="q1", body=body2)["suggest"]["q1"][0]["options"]


if __name__ == '__main__':
	# create_es()
	# index_msg()
	load_msg()
