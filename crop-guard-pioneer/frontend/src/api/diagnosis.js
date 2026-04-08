// 管理“诊断页面需要调用的后端接口
import request from "./request";

export function predictDisease(file, cropType) {
  const formData = new FormData();
  formData.append("file", file);
  if (cropType) {
    formData.append("crop_type", cropType);
  }

  return request.post("/api/v1/diagnosis/predict", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}
