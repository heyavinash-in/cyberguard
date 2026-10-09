# CyberGuard Image Authenticity Benchmark

## Dataset Source
- **Name**: Hemg/AI-Generated-vs-Real-Images-Datasets
- **Platform**: Hugging Face Datasets
- **Selection**: We stream the `train` split and deterministically pick the first valid RGB images to build a balanced 60-image subset (20 REAL, 20 AI_GENERATED, 10 MANIPULATED, 10 ROBUSTNESS).

## Benchmark Composition
- **REAL**: 20 authentic images.
- **AI_GENERATED**: 20 synthetic images.
- **MANIPULATED**: 10 real images aggressively color-enhanced to mimic digital manipulation.
- **ROBUSTNESS**: 10 real images with heavy JPEG compression (quality=40) or 50% resizing.

## Requirements
- Backend API must be running (`cd backend; python -m uvicorn app.main:app --port 8000`)
- `pip install datasets pandas Pillow requests scipy numpy`

## How to Run
```bash
python backend/benchmarks/image_authenticity/scripts/run_benchmark.py
```

## Outputs
All results are stored in `backend/benchmarks/image_authenticity/generated/reports/`:
- `image_authenticity_benchmark_report.md`: Human-readable summary and confusion matrix.
- `benchmark_summary.json`: Machine-readable top-level metrics.
- `results.csv` / `results_raw.json`: Complete row-by-row prediction dump.
- `false_positives.csv` / `false_negatives.csv`: Extraction of errors for quick analysis.
