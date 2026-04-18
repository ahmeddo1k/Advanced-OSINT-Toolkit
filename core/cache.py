import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from config import config
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """مدير التخزين المؤقت (In-Memory & File-based)"""
    
    def __init__(self, ttl=None):
        self.ttl = ttl or config.CACHE_TTL
        self.cache_dir = config.CACHE_DIR
        self.memory_cache = {}
    
    def _generate_key(self, data):
        """توليد مفتاح التخزين المؤقت"""
        hash_obj = hashlib.md5(str(data).encode())
        return hash_obj.hexdigest()
    
    def _get_cache_file(self, key):
        """الحصول على مسار ملف التخزين المؤقت"""
        return self.cache_dir / f"{key}.cache"
    
    def get(self, key):
        """الحصول على البيانات من التخزين المؤقت"""
        if not config.CACHE_ENABLED:
            return None
        
        # التحقق من الذاكرة أولاً
        if key in self.memory_cache:
            data, expiry = self.memory_cache[key]
            if datetime.now() < expiry:
                logger.info(f"💾 Cache hit: {key}")
                return data
            else:
                del self.memory_cache[key]
        
        # التحقق من الملفات
        cache_file = self._get_cache_file(key)
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                expiry = datetime.fromisoformat(cache_data['expiry'])
                if datetime.now() < expiry:
                    logger.info(f"📁 File cache hit: {key}")
                    return cache_data['data']
                else:
                    cache_file.unlink()
            except Exception as e:
                logger.warning(f"خطأ في قراءة الـ cache: {str(e)}")
        
        return None
    
    def set(self, key, value, ttl=None):
        """تخزين البيانات في الذاكرة المؤقتة"""
        if not config.CACHE_ENABLED:
            return
        
        ttl = ttl or self.ttl
        expiry = datetime.now() + timedelta(seconds=ttl)
        
        # حفظ في الذاكرة
        self.memory_cache[key] =
