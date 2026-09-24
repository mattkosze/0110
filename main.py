import json

with open("Storage/platformdata.json") as r:
    data = json.load(r)

print(data)

print(data["MBB"]["desc"])