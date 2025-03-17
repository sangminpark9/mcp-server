import time
from typing import Dict, List, Optional, Any
from app.core.config import settings

class ContextManager:
    """컨텍스트 관리자 - 세션별 대화 컨텍스트 관리"""
    
    def __init__(self):
        self.storage_type = settings.CONTEXT_STORAGE
        self.ttl = settings.CONTEXT_TTL
        
        # 스토리지 유형에 따른 초기화
        if self.storage_type == "memory":
            self.contexts = {}  # 메모리 내 스토리지
            self.timestamps = {}  # 마지막 액세스 타임스탬프
        elif self.storage_type == "redis":
            # Redis 사용 시 초기화 (필요한 경우 구현)
            import redis
            self.redis = redis.Redis(host='localhost', port=6379, db=0)
        elif self.storage_type == "sqlite":
            # SQLite 사용 시 초기화 (필요한 경우 구현)
            import sqlite3
            self.conn = sqlite3.connect('contexts.db')
            self._init_db()
    
    def _init_db(self):
        """SQLite DB 초기화 (필요한 경우)"""
        if self.storage_type == "sqlite":
            cursor = self.conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS contexts (
                session_id TEXT PRIMARY KEY,
                context TEXT,
                timestamp INTEGER
            )
            ''')
            self.conn.commit()
    
    def get_context(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        """세션 ID로 컨텍스트 검색"""
        self._clean_expired()  # 만료된 컨텍스트 정리
        
        if self.storage_type == "memory":
            if session_id in self.contexts:
                self.timestamps[session_id] = time.time()
                return self.contexts[session_id]
            return None
        
        elif self.storage_type == "redis":
            # Redis 구현 (필요시)
            context_json = self.redis.get(f"context:{session_id}")
            if context_json:
                import json
                self.redis.expire(f"context:{session_id}", self.ttl)
                return json.loads(context_json)
            return None
        
        elif self.storage_type == "sqlite":
            # SQLite 구현 (필요시)
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT context FROM contexts WHERE session_id = ?", 
                (session_id,)
            )
            result = cursor.fetchone()
            if result:
                import json
                cursor.execute(
                    "UPDATE contexts SET timestamp = ? WHERE session_id = ?",
                    (int(time.time()), session_id)
                )
                self.conn.commit()
                return json.loads(result[0])
            return None
    
    def update_context(self, session_id: str, context: List[Dict[str, Any]]) -> bool:
        """컨텍스트 업데이트 또는 생성"""
        if self.storage_type == "memory":
            self.contexts[session_id] = context
            self.timestamps[session_id] = time.time()
            return True
        
        elif self.storage_type == "redis":
            # Redis 구현 (필요시)
            import json
            self.redis.setex(
                f"context:{session_id}", 
                self.ttl,
                json.dumps(context)
            )
            return True
        
        elif self.storage_type == "sqlite":
            # SQLite 구현 (필요시)
            import json
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO contexts VALUES (?, ?, ?)",
                (session_id, json.dumps(context), int(time.time()))
            )
            self.conn.commit()
            return True
    
    def delete_context(self, session_id: str) -> bool:
        """컨텍스트 삭제"""
        if self.storage_type == "memory":
            if session_id in self.contexts:
                del self.contexts[session_id]
                del self.timestamps[session_id]
                return True
            return False
        
        elif self.storage_type == "redis":
            # Redis 구현 (필요시)
            return bool(self.redis.delete(f"context:{session_id}"))
        
        elif self.storage_type == "sqlite":
            # SQLite 구현 (필요시)
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM contexts WHERE session_id = ?", 
                (session_id,)
            )
            self.conn.commit()
            return cursor.rowcount > 0
    
    def _clean_expired(self):
        """만료된 컨텍스트 정리"""
        now = time.time()
        
        if self.storage_type == "memory":
            expired = [
                sid for sid, ts in self.timestamps.items() 
                if now - ts > self.ttl
            ]
            for sid in expired:
                del self.contexts[sid]
                del self.timestamps[sid]
        
        elif self.storage_type == "redis":
            # Redis는 자동으로 만료됨
            pass
        
        elif self.storage_type == "sqlite":
            # SQLite 구현 (필요시)
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM contexts WHERE timestamp < ?", 
                (int(now - self.ttl),)
            )
            self.conn.commit()