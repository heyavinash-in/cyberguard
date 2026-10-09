from .pretrained_detector import TransformersImageDetector

_detector_instance = None

def get_detector():
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = TransformersImageDetector()
    return _detector_instance
