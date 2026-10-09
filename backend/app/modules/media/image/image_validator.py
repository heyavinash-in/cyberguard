import os
from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_IMAGE_DIMENSION = 8192

async def validate_image(file: UploadFile) -> Image.Image:
    # 1. Content Type Check
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {file.content_type}")
    
    # 2. File Size Check (Read into memory)
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail=f"File size exceeds maximum allowed ({MAX_FILE_SIZE_MB}MB)")
    
    # Reset pointer for processing
    import io
    file_bytes = io.BytesIO(content)
    
    # 3. Prevent Decompression Bombs
    Image.MAX_IMAGE_PIXELS = MAX_IMAGE_DIMENSION * MAX_IMAGE_DIMENSION
    
    try:
        # 4. Safe Decoding
        img = Image.open(file_bytes)
        img.verify() # Verify integrity without decoding fully
        
        # 5. Dimension limits
        if img.width > MAX_IMAGE_DIMENSION or img.height > MAX_IMAGE_DIMENSION:
            raise HTTPException(status_code=400, detail="Image dimensions exceed maximum limits.")
            
        # Re-open for actual processing after verification
        file_bytes.seek(0)
        img = Image.open(file_bytes)
        img.load() # Force loading to catch truncated images
        
        return img, content
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Corrupted or invalid image file.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")
