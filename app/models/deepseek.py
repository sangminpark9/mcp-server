import os
from typing import Dict, List, Optional, Any

from app.models.base import BaseModel
from app.core.config import settings

class DeepSeekModel(BaseModel):
    """DeepSeek 모델 구현"""
    
    def __init__(self, name: str = "deepseek", model_path: str = None):
        super().__init__(name, model_path or settings.DEEPSEEK_MODEL_PATH)
        self.tokenizer = None
        self.device = "cuda" if self._is_cuda_available() else "cpu"
        
    def _is_cuda_available(self) -> bool:
        """CUDA 사용 가능 여부 확인"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    async def load(self) -> bool:
        """모델 및 토크나이저 로드"""
        try:
            # 실제 DeepSeek 모델 로드 코드
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map="auto" if self.device == "cuda" else None,
                torch_dtype="auto"
            )
            return True
        except Exception as e:
            print(f"DeepSeek 모델 로드 오류: {e}")
            return False
    
    async def generate(self, context: List[Dict[str, Any]], parameters: Dict[str, Any] = None) -> str:
        """텍스트 생성"""
        if self.model is None or self.tokenizer is None:
            await self.load()
        
        # 기본 파라미터 설정
        params = {
            "max_new_tokens": settings.MAX_NEW_TOKENS,
            "temperature": settings.TEMPERATURE,
            "top_p": settings.TOP_P,
            "do_sample": True
        }
        
        # 사용자 파라미터로 업데이트
        if parameters:
            params.update(parameters)
        
        try:
            # 컨텍스트 포맷팅
            prompt = self.format_context(context)
            
            # 토큰화 및 생성
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if self.device == "cuda":
                inputs = inputs.to("cuda")
            
            # 생성
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    **params
                )
            
            # 결과 디코딩
            response = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
            return response
            
        except Exception as e:
            print(f"DeepSeek 생성 오류: {e}")
            return f"오류 발생: {str(e)}"
    
    def get_info(self) -> Dict[str, Any]:
        """모델 정보 반환"""
        return {
            "id": self.name,
            "name": "DeepSeek Model",
            "description": "DeepSeek 기반 대형 언어 모델",
            "capabilities": ["text-generation", "code-generation", "reasoning"],
            "languages": ["en", "ko"]  # 지원 언어
        }
        
    def format_context(self, context: List[Dict[str, Any]]) -> str:
        """DeepSeek 모델에 맞게 컨텍스트 포맷팅"""
        formatted = ""
        
        for message in context:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                formatted += f"<|system|>\n{content}\n"
            elif role == "user":
                formatted += f"<|user|>\n{content}\n"
            elif role == "assistant":
                formatted += f"<|assistant|>\n{content}\n"
        
        # 마지막 응답 유도
        if not formatted.endswith("<|assistant|>\n"):
            formatted += "<|assistant|>\n"
            
        return formatted