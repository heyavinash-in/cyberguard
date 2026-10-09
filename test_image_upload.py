import requests
import numpy as np
from PIL import Image
import io
import json

def test_api():
    # Create dummy image in memory
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    
    files = {'image': ('test.jpg', buf, 'image/jpeg')}
    print("Sending POST request to /api/v1/media/image/analyze...")
    
    try:
        res = requests.post("http://127.0.0.1:8000/api/v1/media/image/analyze", files=files)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print(json.dumps(res.json(), indent=2))
        else:
            print(res.text)
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    test_api()
