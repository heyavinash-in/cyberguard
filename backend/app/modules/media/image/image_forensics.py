import numpy as np
from PIL import Image, ImageFilter
from scipy import fftpack
from typing import Dict, Any, Tuple

def get_image_statistics(img: Image.Image) -> Dict[str, Any]:
    """Calculate basic statistical properties of the image."""
    arr = np.array(img.convert('RGB'))
    
    # Calculate RGB channel means and std devs
    means = np.mean(arr, axis=(0, 1))
    stds = np.std(arr, axis=(0, 1))
    
    # Luminance stats
    gray = np.array(img.convert('L'))
    lum_mean = np.mean(gray)
    lum_std = np.std(gray)
    
    # Edge density
    edges = img.convert('L').filter(ImageFilter.FIND_EDGES)
    edge_density = np.sum(np.array(edges) > 128) / (img.width * img.height)
    
    return {
        "rgb_means": [round(float(m), 2) for m in means],
        "rgb_stds": [round(float(s), 2) for s in stds],
        "luminance_mean": round(float(lum_mean), 2),
        "luminance_std": round(float(lum_std), 2),
        "edge_density": round(float(edge_density), 4)
    }

def analyze_frequency(img: Image.Image) -> Dict[str, Any]:
    """Perform lightweight frequency domain analysis using 2D FFT."""
    # Convert to grayscale and resize to a standard small size for fast FFT
    gray = img.convert('L').resize((256, 256), Image.Resampling.BILINEAR)
    arr = np.array(gray, dtype=float)
    
    # Apply FFT
    f = np.fft.fft2(arr)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    
    h, w = magnitude_spectrum.shape
    cy, cx = h // 2, w // 2
    
    # Calculate energy in bands
    # Low frequency: inner 32x32 region
    # Mid frequency: up to 64x64
    # High frequency: the rest
    
    y, x = np.ogrid[-cy:h-cy, -cx:w-cx]
    dist_from_center = np.sqrt(x*x + y*y)
    
    low_mask = dist_from_center <= 32
    mid_mask = (dist_from_center > 32) & (dist_from_center <= 64)
    high_mask = dist_from_center > 64
    
    low_energy = np.sum(magnitude_spectrum[low_mask])
    mid_energy = np.sum(magnitude_spectrum[mid_mask])
    high_energy = np.sum(magnitude_spectrum[high_mask])
    
    total_energy = low_energy + mid_energy + high_energy
    if total_energy == 0: total_energy = 1
    
    hf_ratio = high_energy / total_energy
    
    # High frequency ratio > 0.45 or < 0.1 is sometimes anomalous for typical photos
    # but not definitive proof.
    if hf_ratio > 0.50:
        freq_anomaly = "STRONG"
    elif hf_ratio > 0.45 or hf_ratio < 0.05:
        freq_anomaly = "MODERATE"
    elif hf_ratio > 0.40 or hf_ratio < 0.10:
        freq_anomaly = "WEAK"
    else:
        freq_anomaly = "NONE"
        
    return {
        "low_frequency_ratio": round(float(low_energy / total_energy), 4),
        "mid_frequency_ratio": round(float(mid_energy / total_energy), 4),
        "high_frequency_ratio": round(float(hf_ratio), 4),
        "frequency_anomaly": freq_anomaly
    }

def analyze_compression_and_noise(img: Image.Image, raw_bytes: bytes) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Analyze compression and noise traits."""
    # We can guess JPEG quality if it's JPEG
    quality = None
    if img.format == 'JPEG':
        # PIL extracts quantization tables if available, but it's complex to map back to a standard 0-100 without a large lookup.
        # So we just note if it's JPEG and its approximate compression ratio.
        pass
        
    compression_ratio = len(raw_bytes) / (img.width * img.height * 3) if img.mode == 'RGB' else len(raw_bytes) / (img.width * img.height)
    
    # Calculate noise via high-pass filter residual
    gray = img.convert('L')
    blurred = gray.filter(ImageFilter.GaussianBlur(radius=2))
    residual = np.abs(np.array(gray, dtype=float) - np.array(blurred, dtype=float))
    
    noise_mean = np.mean(residual)
    noise_std = np.std(residual)
    
    # Extremely low noise could imply AI/synthetic/digital art.
    # Extremely high noise could imply heavy compression or grain.
    if noise_mean < 1.0:
        noise_anomaly = "STRONG"
    elif noise_mean < 2.0:
        noise_anomaly = "MODERATE"
    elif noise_mean < 3.0:
        noise_anomaly = "WEAK"
    else:
        noise_anomaly = "NONE"
        
    # Extremely low compression ratio means heavy compression
    if compression_ratio < 0.05:
        comp_anomaly = "MODERATE"
    elif compression_ratio > 2.0:
        comp_anomaly = "WEAK" # Uncompressed format or extremely dense
    else:
        comp_anomaly = "NONE"
        
    compression = {
        "format": img.format,
        "compression_ratio": round(float(compression_ratio), 4),
        "compression_anomaly": comp_anomaly
    }
    
    noise = {
        "noise_mean": round(float(noise_mean), 4),
        "noise_std": round(float(noise_std), 4),
        "noise_anomaly": noise_anomaly
    }
    
    return compression, noise

def run_all_forensics(img: Image.Image, raw_bytes: bytes) -> Dict[str, Any]:
    stats = get_image_statistics(img)
    freq = analyze_frequency(img)
    comp, noise = analyze_compression_and_noise(img, raw_bytes)
    
    return {
        "statistics": stats,
        "frequency": freq,
        "compression": comp,
        "noise": noise,
        "texture": {}
    }
