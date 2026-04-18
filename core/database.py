from sqlalchemy import create_engine, Column, String, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import config
import logging

logger = logging.getLogger(__name__)

# إنشاء base للـ models
Base = declarative_base()

# إنشاء الـ engine
engine = create_engine(
    config.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SearchResult(Base):
    """نموذج نتائج البحث"""
    __tablename__ = "search_results"
    
    id = Column(Integer, primary_key=True, index=True)
    search_type = Column(String, index=True)  # phone, email, domain, etc
    search_query = Column(String, index=True)
    result_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String)  # success, failed, pending
    source = Column(String)  # API name
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.search_type,
            "query": self.search_query,
            "data": self.result_data,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "source": self.source
        }

class CachedData(Base):
    """نموذج البيانات المخزنة مؤقتاً"""
    __tablename__ = "cached_data"
    
    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True)
    cache_value = Column(JSON)
    expiry_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """تهيئة قاعدة البيانات"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ تم تهيئة قاعدة البيانات")
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة قاعدة البيانات: {str(e)}")

def get_db():
    """الحصول على session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_search_result(search_type, query, result_data, status="success", source="internal"):
    """حفظ نتيجة البحث"""
    db = SessionLocal()
    try:
        result = SearchResult(
            search_type=search_type,
            search_query=query,
            result_data=result_data,
            status=status,
            source=source
        )
        db.add(result)
        db.commit()
        logger.info(f"✅ تم حفظ النتيجة: {search_type} - {query}")
        return result.id
    except Exception as e:
        logger.error(f"❌ خطأ في حفظ النتيجة: {str(e)}")
        db.rollback()
    finally:
        db.close()
