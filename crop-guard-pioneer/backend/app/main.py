# 后端总开关，负责启动应用、挂接口、配跨域
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.diagnosis import router as diagnosis_router

app = FastAPI(
    title="Crop Guard Pioneer API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    diagnosis_router,
    prefix="/api/v1/diagnosis",
    tags=["Diagnosis"]
)

@app.get("/ping")
def ping():
    return {"message": "pong"}

