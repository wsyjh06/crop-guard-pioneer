# 定义“诊断接口的响应数据结构”
from typing import List, Optional
from pydantic import BaseModel


class TopPrediction(BaseModel):
    class_name: str
    score: float


class DiagnosisResponse(BaseModel):
    filename: str
    crop_type: Optional[str] = None
    disease_name: str
    confidence: float
    risk_level: str
    symptom_summary: str
    top3: List[TopPrediction]
