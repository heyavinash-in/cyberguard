import shutil
import os

source_dir = r"C:\Users\phoen\.gemini\antigravity\brain\fec4ed6c-450a-40ea-ac6e-f4aafc888768"
target_dir = os.path.join(os.getcwd(), "public", "images")

os.makedirs(target_dir, exist_ok=True)

# find the latest files starting with our names
def find_latest(prefix):
    files = [f for f in os.listdir(source_dir) if f.startswith(prefix) and f.endswith(".jpg")]
    if not files: return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(source_dir, x)), reverse=True)
    return os.path.join(source_dir, files[0])

files_to_copy = {
    "dashboard_vector": "dashboard.jpg",
    "url_scanner_vector": "url_scanner.jpg",
    "message_vector": "message.jpg",
    "media_vector": "media.jpg"
}

for prefix, target_name in files_to_copy.items():
    src = find_latest(prefix)
    if src:
        dst = os.path.join(target_dir, target_name)
        shutil.copy2(src, dst)
        print(f"Copied {src} to {dst}")
    else:
        print(f"Could not find {prefix}")
