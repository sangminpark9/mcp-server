from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class BaseModel(ABC):
    """모든 LLM 모델의 기본 인터페이스"""
    
    def __init__(self, name: str, model_path: str):
        self.name = name
        self.model_path = model_path
        self.model = None  # 실제 모델 인스턴스
    
    @abstractmethod
    async def load(self) -> bool:
        """모델 로드"""
        pass
    
    @abstractmethod
    async def generate(self, context: List[Dict[str, Any]], parameters: Dict[str, Any] = None) -> str:
        """텍스트 생성"""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """모델 정보 반환"""
        pass
    
    def format_context(self, context: List[Dict[str, Any]]) -> str:
        """
        컨텍스트를 모델 입력으로 변환
        기본 구현은 간단한 텍스트 연결, 각 모델별로 오버라이드 가능
        """
        formatted = ""
        for message in context:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                formatted += f"<system>\n{content}\n</system>\n\n"
            elif role == "user":
                formatted += f"<human>\n{content}\n</human>\n\n"
            elif role == "assistant":
                formatted += f"<assistant>\n{content}\n</assistant>\n\n"
        
        # 마지막 응답 유도
        formatted += "<assistant>\n"
        return formatted