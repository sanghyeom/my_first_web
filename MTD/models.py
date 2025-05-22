from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone

from database import Base


# DB에 저장될 'User' 테이블의 형태를 파이썬 클래스로 정의 (ORM 모델)
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True) 
    identification = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

    posts = relationship("Post", back_populates="author") # User 모델의 relationship!
    
    def __repr__(self):
        return f"<User(id={self.id}, identification='{self.identification}')>"
# --- 여기! DB 세션을 제공하는 의존성 함수 get_db() 추가 ---
def get_db():
    db = SessionLocal() # DB 세션 생성
    try:
        yield db # 세션 객체를 요청 핸들러로 넘겨주고 잠시 대기
    finally:
        db.close() # 요청 처리 끝나면 세션 닫기!
        print("➡️ DB 세션 종료.") # 디버깅용 출력
# --- 여기까지 DB 모델 정의 ---

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    views = Column(Integer, default=0, nullable=False)

    author = relationship("User", back_populates="posts")

