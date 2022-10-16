import json
amount = 0
with open("new_m2.json","w",encoding="utf-8") as f:
  with open ("m2.json") as raw_dict:
    d = json.load(raw_dict)
    for v in d:
      amount += 1
    for v in json.JSONEncoder(ensure_ascii=False,indent=4).iterencode(d):
      f.write(v)
print(f"[+] Total vacancies: {amount}")
