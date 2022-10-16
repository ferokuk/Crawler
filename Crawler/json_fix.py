import json


amount = 0
with open("machinist_result.json","w",encoding="utf-8") as f:
  with open ("m.json") as raw_dict:
    d = json.load(raw_dict)
    for v in d:
      amount += 1
    for v in json.JSONEncoder(ensure_ascii=False,indent=4).iterencode(d):
      f.write(v)
print(f"[+] Total machinist vacancies: {amount}")

amount = 0
with open("cooks_result.json","w",encoding="utf-8") as f:
  with open ("c.json") as raw_dict:
    d = json.load(raw_dict)
    for v in d:
      amount += 1
    for v in json.JSONEncoder(ensure_ascii=False,indent=4).iterencode(d):
      f.write(v)
print(f"[+] Total cooks vacancies: {amount}")
