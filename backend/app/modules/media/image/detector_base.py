from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from PIL import Image

class ImageAuthenticityDetectorBase(ABC):
    """
    Base class for image authenticity detectors.
    """
    
    @abstractmethod
    def load(self) -> None:
        """Load the model into memory. Should be idempotent."""
        pass
        
    @abstractmethod
    def predict(self, image: Image.Image) -> Tuple[str, float, float, Dict[str, Any]]:
        """
        Run inference on the image.
        Returns:
            classification: "REAL", "AI_GENERATED", or "UNCERTAIN"
            ai_probability: Float between 0 and 1
            real_probability: Float between 0 and 1
            metadata: Dict containing model info (name, version, inference_ms)
        """
        pass
        
    @abstractmethod
    def health_check(self) -> bool:
        """Check if model is loaded and healthy."""
        pass
        
    @abstractmethod
    def model_info(self) -> Dict[str, str]:
        """Return static model information."""
        pass
