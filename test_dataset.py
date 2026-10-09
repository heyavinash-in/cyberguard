import os
import time
from backend.app.modules.media.image.image_authenticity_service import analyze_image
from PIL import Image
import io
from datasets import load_dataset
import logging

# Disable unnecessary logging
logging.getLogger("transformers").setLevel(logging.ERROR)

def evaluate():
    print("==================================================")
    print("CYBERGUARD IMAGE AUTHENTICITY 60-IMAGE BENCHMARK")
    print("==================================================")
    
    total = 60
    ai_count = 30
    real_count = 30
    
    results = {
        "true_positives": 0,
        "false_positives": 0,
        "true_negatives": 0,
        "false_negatives": 0,
        "uncertain": 0,
        "failures": 0
    }
    
    print(f"Preparing to test {total} images ({ai_count} AI, {real_count} Real)...")
    print("Streaming dataset from HuggingFace Hub (Hemg/AI-Generated-vs-Real-Images-Datasets)...")
    
    try:
        # Load dataset
        dataset = load_dataset("Hemg/AI-Generated-vs-Real-Images-Datasets", split="train", streaming=True)
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return
        
    ai_tested = 0
    real_tested = 0
    i = 0
    
    for item in dataset:
        if ai_tested >= ai_count and real_tested >= real_count:
            break
            
        label = item.get('label')
        # Hemg dataset: 0 = Real, 1 = Fake (AI) generally. Let's verify:
        # We will assume 1 is AI.
        is_ai_ground_truth = (label == 1)
        
        if is_ai_ground_truth and ai_tested >= ai_count:
            continue
        if not is_ai_ground_truth and real_tested >= real_count:
            continue
            
        img = item['image']
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        img_bytes = buf.getvalue()
        
        try:
            start = time.time()
            res = analyze_image(img, img_bytes)
            latency = (time.time() - start) * 1000
            
            pred_label = res.classification
            print(f"Image {i+1:02d} | Ground Truth: {'AI' if is_ai_ground_truth else 'REAL'} | Prediction: {pred_label} | Score: {res.risk_score} | Latency: {latency:.1f}ms")
            
            if pred_label == "AI_GENERATED":
                if is_ai_ground_truth:
                    results["true_positives"] += 1
                else:
                    results["false_positives"] += 1
            elif pred_label == "REAL":
                if not is_ai_ground_truth:
                    results["true_negatives"] += 1
                else:
                    results["false_negatives"] += 1
            else:
                results["uncertain"] += 1
                
        except Exception as e:
            print(f"Image {i+1:02d} | Error: {e}")
            results["failures"] += 1
            
        if is_ai_ground_truth:
            ai_tested += 1
        else:
            real_tested += 1
        i += 1
            
    print("==================================================")
    print("BENCHMARK RESULTS")
    print("==================================================")
    
    tp = results["true_positives"]
    fp = results["false_positives"]
    tn = results["true_negatives"]
    fn = results["false_negatives"]
    
    accuracy = (tp + tn) / max(total - results["uncertain"] - results["failures"], 1)
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    
    print(f"Total Tested: {ai_tested + real_tested}")
    print(f"True Positives (AI correctly flagged): {tp}")
    print(f"True Negatives (Real correctly passed): {tn}")
    print(f"False Positives (Real falsely flagged): {fp}")
    print(f"False Negatives (AI falsely passed): {fn}")
    print(f"Uncertain: {results['uncertain']}")
    print(f"Failures: {results['failures']}")
    print("--------------------------------------------------")
    print(f"Accuracy (excl. uncertain): {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall: {recall * 100:.2f}%")
    print("==================================================")

if __name__ == "__main__":
    evaluate()
