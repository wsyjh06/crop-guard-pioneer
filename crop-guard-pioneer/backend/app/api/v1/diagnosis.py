# 定义“诊断接口”
# “前端上传图片后，后端要响应哪个 URL、怎么接收参数
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.diagnosis import DiagnosisResponse
from app.services.diagnosis_service import predict_disease

router = APIRouter()


@router.post("/predict", response_model=DiagnosisResponse)
async def predict(
    file: UploadFile = File(...),
    crop_type: str | None = Form(None),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    result = predict_disease(file=file, crop_type=crop_type)
    return result
