from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from typing import Dict, List, Optional, Any

from app.schemas.requests import (
    ChatRequest, ChatResponse, 
    ModelInfo, AvailableModelsResponse
)
from app.core.context import ContextManager
from app.models.router import ModelRouter

router = APIRouter()
context_manager = ContextManager()
model_router = ModelRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    메인 채팅 엔드포인트 - 요청에 따라 적절한 모델로 라우팅
    """
    # 세션 ID가 없으면 새로 생성
    if not request.session_id:
        request.session_id = str(uuid4())
    
    # 컨텍스트 검색 또는 생성
    context = context_manager.get_context(request.session_id)
    if not context and request.messages:
        context = []
    
    # 메시지가 있으면 컨텍스트에 추가
    if request.messages:
        context.extend(request.messages)
        context_manager.update_context(request.session_id, context)
    
    # 모델 결정 (태스크 또는 요청에 따라)
    model_name = request.model if request.model else "default"
    model = model_router.get_model(model_name)
    
    # 모델 추론 실행
    try:
        response = await model.generate(
            context=context,
            parameters=request.parameters or {}
        )
        
        # 응답을 컨텍스트에 추가 (필요한 경우)
        if request.save_context and response:
            context.append({"role": "assistant", "content": response})
            context_manager.update_context(request.session_id, context)
        
        return ChatResponse(
            session_id=request.session_id,
            response=response,
            model=model.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"모델 추론 오류: {str(e)}")

@router.get("/models", response_model=AvailableModelsResponse)
async def list_models():
    """
    사용 가능한 모델 목록 반환
    """
    models = model_router.list_models()
    return AvailableModelsResponse(models=models)

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    세션 및 관련 컨텍스트 삭제
    """
    success = context_manager.delete_context(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"세션 ID {session_id}를 찾을 수 없습니다")
    return {"status": "success", "message": f"세션 {session_id}가 삭제되었습니다"}