from typing import Dict, List, Optional, Any

from app.models.base import BaseModel
from app.models.deepseek import DeepSeekModel
from app.models.llama import LlamaModel
from app.core.config import settings

class ModelRouter:
    """
    모델 라우터 - 요청에 따라 적절한 모델로 라우팅
    """
    
    def __init__(self):
        self.models = {}
        self.routing_map = settings.MODEL_ROUTING
        self._initialize_models()
    
    def _initialize_models(self):
        """기본 모델 초기화"""
        # DeepSeek 모델 등록
        self.models["deepseek"] = DeepSeekModel()
        
        # Llama 모델 등록
        self.models["llama"] = LlamaModel()
    
    def get_model(self, model_identifier: str) -> BaseModel:
        """
        모델 식별자에 따라 적절한 모델 반환
        """
        # 라우팅 맵에서 실제 모델 이름 찾기
        model_name = self.routing_map.get(model_identifier, model_identifier)
        
        # 모델이 존재하면 반환, 없으면 기본 모델 반환
        if model_name in self.models:
            return self.models[model_name]
        else:
            # 기본 모델은 "default" 키에 매핑된 모델
            default_model = self.routing_map.get("default", "deepseek")
            return self.models[default_model]
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        사용 가능한 모델 목록과 정보 반환
        """
        return [model.get_info() for model in self.models.values()]
    
    def add_model(self, model_name: str, model: BaseModel) -> bool:
        """
        새 모델 추가
        """
        if model_name in self.models:
            return False
        
        self.models[model_name] = model
        return True
    
    def remove_model(self, model_name: str) -> bool:
        """
        모델 제거
        """
        if model_name in self.models:
            del self.models[model_name]
            return True
        return False