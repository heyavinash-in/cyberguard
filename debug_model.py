import io
from datasets import load_dataset
from transformers import pipeline

dataset = load_dataset("JingmingWang/AI-generated-Image-Detection", split="train", streaming=True)
p = pipeline("image-classification", model="prithivMLmods/Deep-Fake-Detector-Model")

for idx, item in enumerate(dataset):
    if idx >= 3:
        break
    img = item['image']
    if img.mode != "RGB":
        img = img.convert("RGB")
    res = p(img)
    print(f"Image {idx}: Label={item.get('label')}")
    print(f"Model Output: {res}")
