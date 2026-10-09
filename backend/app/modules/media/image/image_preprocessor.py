from PIL import Image, ImageOps

def preprocess_image(img: Image.Image, target_size=(224, 224)) -> Image.Image:
    """
    Standardize image for model ingestion:
    1. EXIF orientation correction
    2. Convert to RGB
    3. Center crop to target size
    """
    # 1. Correct EXIF orientation
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
        
    # 2. Convert to RGB (drops alpha channel for PNG/WEBP safely)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    # 3. Resize & Crop
    # Fit the image into the target box, cropping from center to maintain aspect ratio
    img = ImageOps.fit(img, target_size, method=Image.Resampling.BICUBIC, centering=(0.5, 0.5))
    
    return img
