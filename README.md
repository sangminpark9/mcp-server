# MCP (Model Context Protocol) 서버

MCP 서버는 다양한 LLM(Large Language Model)을 통합 관리하고 표준화된 인터페이스를 제공하는 서비스입니다. 이 프로젝트는 DeepSeek와 Llama 모델을 통합하여 모델 간 전환이 용이하고, 컨텍스트 관리가 가능한 API를 제공합니다.

## 주요 기능

- 다양한 LLM 모델(DeepSeek, Llama) 통합 관리
- 모델 간 쉬운 전환 및 라우팅
- 대화 컨텍스트 관리
- 표준화된 API 인터페이스
- 다양한 스토리지 백엔드 지원(메모리, Redis, SQLite)

## 시스템 요구사항

- Python 3.8 이상
- CUDA 지원 GPU (권장, CPU에서도 실행 가능)
- Docker & Docker Compose (선택 사항)

## 설치 및 실행

### 수동 설치

1. 저장소 클론:
   ```bash
   git clone https://github.com/yourusername/mcp-server.git
   cd mcp-server
   ```

2. 설정 스크립트 실행:
   ```bash
   python setup.py
   ```
   
   (모델 다운로드 포함):
   ```bash
   python setup.py --download-models
   ```
   
   (특정 모델만 다운로드):
   ```bash
   python setup.py --download-models --model deepseek
   ```

3. 서버 실행:
   ```bash
   source venv/bin/activate  # Windows: venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

### Docker를 사용한 설치

1. 저장소 클론:
   ```bash
   git clone https://github.com/yourusername/mcp-server.git
   cd mcp-server
   ```

2. Docker Compose로 실행:
   ```bash
   docker-compose up -d
   ```

## API 사용법

### 채팅 API

**요청:**
```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "role": "user",
      "content": "안녕하세요, 오늘 날씨가 어때요?"
    }
  ],
  "model": "default",
  "parameters": {
    "temperature": 0.7,
    "max_new_tokens": 512
  }
}
```

**응답:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "안녕하세요! 오늘 날씨는 맑고 화창하네요. 온도는 약 22도 정도로 쾌적한 편입니다. 야외 활동하기 좋은 날씨입니다.",
  "model": "deepseek"
}
```

### 사용 가능한 모델 목록

**요청:**
```http
GET /api/models
```

**응답:**
```json
{
  "models": [
    {
      "id": "deepseek",
      "name": "DeepSeek Model",
      "description": "DeepSeek 기반 대형 언어 모델",
      "capabilities": ["text-generation", "code-generation", "reasoning"],
      "languages": ["en", "ko"]
    },
    {
      "id": "llama",
      "name": "Llama Model",
      "description": "Llama 기반 대형 언어 모델 (한국어 특화)",
      "capabilities": ["text-generation", "translation", "korean-language"],
      "languages": ["ko", "en"]
    }
  ]
}
```

### 세션 삭제

**요청:**
```http
DELETE /api/sessions/550e8400-e29b-41d4-a716-446655440000
```

**응답:**
```json
{
  "status": "success",
  "message": "세션 550e8400-e29b-41d4-a716-446655440000가 삭제되었습니다"
}
```

## 모델 추가하기

새로운 모델을 추가하려면:

1. `app/models` 디렉토리에 새 모델 클래스 파일을 생성합니다.
2. `BaseModel` 클래스를 상속받아 구현합니다.
3. `app/models/router.py`에서 모델을 등록합니다.
4. `app/core/config.py`에서 라우팅 설정을 업데이트합니다.

## 기여 방법

1. 저장소를 포크합니다.
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`).
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`).
5. Pull Request를 생성합니다.