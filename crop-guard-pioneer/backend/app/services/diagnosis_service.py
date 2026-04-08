from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import UploadFile

from app.schemas.diagnosis import DiagnosisResponse, TopPrediction

UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _mock_result(crop_type: str | None) -> DiagnosisResponse:
    crop = (crop_type or "").strip().lower()

    if crop == "rice":
        return DiagnosisResponse(
            filename="",
            crop_type="rice",
            disease_name="Rice Blast",
            confidence=0.91,
            risk_level="high",
            symptom_summary="Leaf lesions are spindle-shaped and disease spread risk is relatively high.",
            top3=[
                TopPrediction(class_name="Rice Blast", score=0.91),
                TopPrediction(class_name="Brown Spot", score=0.06),
                TopPrediction(class_name="Leaf Smut", score=0.03),
            ],
        )

    if crop == "tomato":
        return DiagnosisResponse(
            filename="",
            crop_type="tomato",
            disease_name="Tomato Early Blight",
            confidence=0.87,
            risk_level="medium",
            symptom_summary="Circular spots with concentric rings are observed on leaves.",
            top3=[
                TopPrediction(class_name="Tomato Early Blight", score=0.87),
                TopPrediction(class_name="Tomato Septoria Leaf Spot", score=0.08),
                TopPrediction(class_name="Tomato Healthy", score=0.05),
            ],
        )

    return DiagnosisResponse(
        filename="",
        crop_type=crop_type,
        disease_name="Corn Common Rust",
        confidence=0.82,
        risk_level="medium",
        symptom_summary="Suspected rust-like lesions detected on leaf surface.",
        top3=[
            TopPrediction(class_name="Corn Common Rust", score=0.82),
            TopPrediction(class_name="Corn Gray Leaf Spot", score=0.11),
            TopPrediction(class_name="Corn Healthy", score=0.07),
        ],
    )


def predict_disease(file: UploadFile, crop_type: str | None = None) -> DiagnosisResponse:
    suffix = Path(file.filename).suffix.lower() or ".jpg"
    stored_name = f"{uuid4().hex}{suffix}"
    save_path = UPLOAD_DIR / stored_name

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = _mock_result(crop_type)
    result.filename = stored_name
    return result
