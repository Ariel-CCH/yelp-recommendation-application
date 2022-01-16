import json
 
f = open('graph.json')
data = json.load(f)
print(data)
 
f.close()