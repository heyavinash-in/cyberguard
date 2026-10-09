import urllib.request
import re

url = 'https://www.kaggle.com/code/ddosad/spam-email-classifier'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
import json
# Look for Kaggle.State
m = re.search(r'window\.Kaggle\.State = (\{.*?\});', html)
if m:
    data = json.loads(m.group(1))
    print(json.dumps(data, indent=2)[:1000])
    with open('kaggle_state.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
else:
    print("No Kaggle.State found")
