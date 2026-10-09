import hashlib
from PIL import Image, ExifTags
from typing import Dict, Any

def extract_image_metadata(img: Image.Image, raw_bytes: bytes) -> Dict[str, Any]:
    """
    Extract non-invasive metadata and calculate hash.
    """
    meta = {
        "width": img.width,
        "height": img.height,
        "aspect_ratio": round(img.width / img.height, 4) if img.height > 0 else 0,
        "mode": img.mode,
        "format": img.format,
        "file_size_bytes": len(raw_bytes),
        "sha256": hashlib.sha256(raw_bytes).hexdigest()
    }
    
    # Extract EXIF if available safely
    exif_data = {}
    has_exif = False
    try:
        exif = img.getexif()
        if exif is not None:
            has_exif = True
            for k, v in exif.items():
                if k in ExifTags.TAGS:
                    tag_name = ExifTags.TAGS[k]
                    # Filter out giant binary blobs like MakerNote or UserComment for safety
                    if tag_name not in ['MakerNote', 'UserComment']:
                        # Ensure value is easily serializable
                        if isinstance(v, (int, float, str)):
                            exif_data[tag_name] = v
                        elif isinstance(v, tuple) and all(isinstance(x, (int, float)) for x in v):
                            exif_data[tag_name] = list(v)
    except Exception:
        pass # Corrupted or unsupported EXIF is ignored safely
        
    meta["has_exif"] = has_exif
    if has_exif:
        meta["exif"] = exif_data
        
    return meta
