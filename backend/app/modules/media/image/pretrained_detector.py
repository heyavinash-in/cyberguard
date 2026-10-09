import time
import os
from typing import Tuple, Dict, Any
from PIL import Image

from .detector_base import ImageAuthenticityDetectorBase
from .image_preprocessor import preprocess_image

class TransformersImageDetector(ImageAuthenticityDetectorBase):
    def __init__(self, model_name: str = "prithivMLmods/Deep-Fake-Detector-Model", device: str = "cpu"):
        self.model_name = os.environ.get("MEDIA_IMAGE_DETECTOR_MODEL", model_name)
        self.device = os.environ.get("MEDIA_IMAGE_DETECTOR_DEVICE", device)
        
        self.uncertainty_threshold_low = float(os.environ.get("MEDIA_IMAGE_DETECTOR_UNCERTAINTY_LOW", "0.20"))
        self.uncertainty_threshold_high = float(os.environ.get("MEDIA_IMAGE_DETECTOR_UNCERTAINTY_HIGH", "0.80"))
        
        self.pipeline = None
        self._is_loaded = False
        
    def load(self) -> None:
        if self._is_loaded:
            return
            
        import torch
        from transformers import pipeline
        
        # Determine torch device
        torch_device = -1 if self.device == "cpu" else 0
        
        # Load pipeline
        # We load image-classification pipeline
        self.pipeline = pipeline("image-classification", model=self.model_name, device=torch_device)
        self._is_loaded = True

    def _normalize_output(self, hf_results: list) -> Tuple[str, float, float]:
        """
        Takes huggingface results like:
        [{'label': 'artificial', 'score': 0.9}, {'label': 'human', 'score': 0.1}]
        and normalizes it.
        """
        ai_prob = 0.0
        real_prob = 0.0
        
        # Known labels for various popular models
        ai_labels = {'artificial', 'fake', 'ai', 'ai_generated', 'generated', '1'}
        real_labels = {'human', 'real', 'authentic', 'nature', '0'}
        
        for res in hf_results:
            label = res['label'].lower()
            score = res['score']
            
            if label in ai_labels:
                ai_prob += score
            elif label in real_labels:
                real_prob += score
            else:
                # If the model has labels like 'fake' and 'real', we match those.
                # If unknown, just fallback.
                if 'ai' in label or 'fake' in label:
                    ai_prob += score
                else:
                    real_prob += score
                    
        # Normalize to 1.0 just in case
        total = ai_prob + real_prob
        if total > 0:
            ai_prob /= total
            real_prob /= total
            
        # Apply uncertainty zone
        if ai_prob >= self.uncertainty_threshold_high:
            classification = "AI_GENERATED"
        elif ai_prob <= self.uncertainty_threshold_low:
            classification = "REAL"
        else:
            classification = "UNCERTAIN"
            
        return classification, ai_prob, real_prob

    def predict(self, image: Image.Image) -> Tuple[str, float, float, Dict[str, Any]]:
        self.load()
        
        start_time = time.time()
        
        # We let the HF pipeline do its own preprocessing (feature extractor),
        # but we pass it the safe decoded RGB image from our validator.
        # Ensure it is RGB as pipeline expects RGB.
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        results = self.pipeline(image)
        
        end_time = time.time()
        inference_ms = int((end_time - start_time) * 1000)
        
        classification, ai_prob, real_prob = self._normalize_output(results)
        
        metadata = {
            "name": self.model_name,
            "version": "huggingface",
            "inference_ms": inference_ms
        }
        
        return classification, ai_prob, real_prob, metadata
        
    def health_check(self) -> bool:
        return self._is_loaded and self.pipeline is not None
        
    def model_info(self) -> Dict[str, str]:
        return {
            "name": self.model_name,
            "type": "transformers-pipeline",
            "device": self.device
        }
