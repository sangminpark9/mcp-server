from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union

class Message(BaseModel):
    role: str  # "user", "assistant", "system" 등
    content: str
    
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    messages: List[Message] = []
    model: Optional[str] = None  # 사용할 모델, None이면 기본값 사용
    parameters: Optional[Dict[str, Any]] = None  # 온도, top_p 등 모델 파라미터
    save_context: bool = True  # 컨텍스트에 응답 저장 여부
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "messages": [
                    {"role": "user", "content": "안녕하세요, 오늘 날씨가 어때요?"}
                ],
                "model": "default",
                "parameters": {"temperature": 0.7, "max_new_tokens": 512},
                "save_context": True
            }
        }

class ChatResponse(BaseModel):
    session_id: str
    response: str
    model: str
    
class ModelInfo(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    capabilities: List[str] = []
    languages: List[str] = []
    
class AvailableModelsResponse(BaseModel):
    models: List[ModelInfo]