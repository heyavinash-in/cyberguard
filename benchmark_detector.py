import os
import time
import psutil
import numpy as np
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

from backend.app.modules.media.image.pretrained_detector import TransformersImageDetector
from backend.app.modules.media.image.image_validator import validate_image
from backend.app.modules.media.image.image_authenticity_service import analyze_image

# Set env to use local caching or specific model
os.environ["MEDIA_IMAGE_DETECTOR_MODEL"] = "umm-maybe/AI-image-detector"
os.environ["MEDIA_IMAGE_DETECTOR_DEVICE"] = "cpu"

def get_ram_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def run_benchmark():
    print("--- CYBERGUARD IMAGE AUTHENTICITY BENCHMARK ---")
    
    # 1. Measure RAM before load
    ram_before = get_ram_mb()
    print(f"RAM Before Load: {ram_before:.2f} MB")
    
    # Create random synthetic image for benchmarking
    # A generic real/fake prediction requires an actual RGB image
    print("Generating synthetic 512x512 image for benchmarking...")
    img = Image.fromarray(np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8))
    
    # 2. Cold Start
    detector = TransformersImageDetector()
    print(f"Loading model: {detector.model_name} on {detector.device}...")
    
    start_cold = time.time()
    detector.load()
    end_cold = time.time()
    cold_start_time = end_cold - start_cold
    
    ram_after = get_ram_mb()
    print(f"RAM After Load: {ram_after:.2f} MB (Delta: {ram_after - ram_before:.2f} MB)")
    print(f"Cold Start Time: {cold_start_time:.3f} s")
    
    # 3. Warm Inferences
    num_warmups = 2
    print(f"Running {num_warmups} warmup inferences...")
    for _ in range(num_warmups):
        detector.predict(img)
        
    num_benchmarks = 10
    print(f"Running {num_benchmarks} measured inferences (Full Pipeline including forensics)...")
    latencies = []
    
    # Save the img as a safe upload equivalent
    import io
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    raw_bytes = buf.getvalue()
    
    for _ in range(num_benchmarks):
        start = time.time()
        result = analyze_image(img, raw_bytes)
        end = time.time()
        latencies.append((end - start) * 1000)
        
    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)
    
    print("\n--- BENCHMARK RESULTS ---")
    print(f"MODEL: {detector.model_name}")
    print(f"DEVICE: {detector.device}")
    print(f"IMAGE RESOLUTION: 512x512 -> pipeline standard")
    print(f"COLD START TIME: {cold_start_time:.3f} s")
    print(f"WARM FULL-PIPELINE TIME (P50): {p50:.2f} ms")
    print(f"WARM FULL-PIPELINE TIME (P95): {p95:.2f} ms")
    print(f"RAM INCREASE: {ram_after - ram_before:.2f} MB")
    print(f"TEST OUTPUT: Classification={result.classification}, AI_Prob={result.ai_probability:.3f}, Real_Prob={result.real_probability:.3f}")

if __name__ == "__main__":
    run_benchmark()
