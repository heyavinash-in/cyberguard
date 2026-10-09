import urllib.request
import json
import os

url = 'https://raw.githubusercontent.com/Ashutoshx7/VengeanceUI/main/public/r/perspective-carousel.json'
try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    file_content = data['files'][0]['content']
    file_path = os.path.join('src', 'components', 'ui', 'perspective-carousel.tsx')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print("Downloaded successfully to:", file_path)
except Exception as e:
    print("Error:", e)
