import json

with open("new_cooks.json","w",encoding="utf-8") as f:
  with open ("cooks.json") as raw_dict:
    d = json.load(raw_dict)
    for v in json.JSONEncoder(ensure_ascii=False,indent=4).iterencode(d):
      f.write(v)
