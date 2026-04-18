import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class Config:
    """إعدادات البرنامج الرئيسية"""
    
    # معلومات التطبيق
    APP_NAME = "Advanced OSINT Toolkit"
    APP_VERSION = "3.0.0"
    APP_DESCRIPTION = "Professional Digital Intelligence Gathering Tool"
    
    # المسارات
    BASE_DIR = Path(__file__).resolve().parent
    REPORTS_DIR = BASE_DIR / "reports"
    LOGS_DIR = BASE_DIR / "logs"
    DATABASE_DIR = BASE_DIR / "database"
    CACHE_DIR = BASE_DIR / ".cache"
    
    # إنشاء المجلدات
    for directory in [REPORTS_DIR, LOGS_DIR, DATABASE_DIR, CACHE_DIR]:
        directory.mkdir(exist_ok=True)
    
    # قاعدة البيانات
    DATABASE_URL = f"sqlite:///{DATABASE_DIR}/osint.db"
    
    # معلومات السجل
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    MAX_LOG_SIZE = 10485760  # 10 MB
    BACKUP_COUNT = 5
    
    # إعدادات الطلبات (Requests)
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    RATE_LIMIT_DELAY = int(os.getenv("RATE_LIMIT_DELAY", 1))
    
    # إعدادات التخزين المؤقت (Cache)
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 ساعة
    
    # المنصات الاجتماعية المدعومة
    SOCIAL_PLATFORMS = {
        "instagram": {
            "url": "https://instagram.com/{}",
            "api": "https://i.instagram.com/api/v1/users/web_profile_info/",
            "enabled": True
        },
        "github": {
            "url": "https://github.com/{}",
            "api": "https://api.github.com/users/{}",
            "enabled": True
        },
        "twitter": {
            "url": "https://x.com/{}",
            "api": "https://api.twitter.com/2/users/by/username/{}",
            "enabled": os.getenv("TWITTER_API_KEY") is not None
        },
        "linkedin": {
            "url": "https://linkedin.com/in/{}",
            "api": None,
            "enabled": True
        },
        "tiktok": {
            "url": "https://tiktok.com/@{}",
            "api": "https://www.tiktok.com/api/user/detail/{}",
            "enabled": True
        },
        "youtube": {
            "url": "https://youtube.com/@{}",
            "api": None,
            "enabled": True
        },
        "reddit": {
            "url": "https://reddit.com/user/{}",
            "api": "https://www.reddit.com/user/{}/about.json",
            "enabled": True
        },
        "twitch": {
            "url": "https://twitch.tv/{}",
            "api": "https://api.twitch.tv/helix/users",
            "enabled": os.getenv("TWITCH_CLIENT_ID") is not None
        }
    }
    
    # APIs الخارجية
    EXTERNAL_APIS = {
        "ipapi": {
            "enabled": True,
            "key": os.getenv("IPAPI_KEY"),
            "url": "https://ipapi.co/{}/json/"
        },
        "abuseipdb": {
            "enabled": os.getenv("ABUSEIPDB_KEY") is not None,
            "key": os.getenv("ABUSEIPDB_KEY"),
            "url": "https://api.abuseipdb.com/api/v2/check"
        },
        "shodan": {
            "enabled": os.getenv("SHODAN_KEY") is not None,
            "key": os.getenv("SHODAN_KEY"),
            "url": "https://api.shodan.io/shodan/host/{}"
        },
        "virustotal": {
            "enabled": os.getenv("VIRUSTOTAL_KEY") is not None,
            "key": os.getenv("VIRUSTOTAL_KEY"),
            "url": "https://www.virustotal.com/api/v3/"
        },
        "hunter": {
            "enabled": os.getenv("HUNTER_KEY") is not None,
            "key": os.getenv("HUNTER_KEY"),
            "url": "https://api.hunter.io/v2/"
        }
    }
    
    # إعدادات البحث
    SEARCH_TIMEOUT = 30
    MAX_RESULTS = 100
    DEEP_SEARCH = os.getenv("DEEP_SEARCH", "false").lower() == "true"
    
    # الأمان
    VERIFY_SSL = os.getenv("VERIFY_SSL", "true").lower() == "true"
    PROXY_ENABLED = os.getenv("PROXY_ENABLED", "false").lower() == "true"
    PROXY_URL = os.getenv("PROXY_URL")
    
    # تنسيق التقارير
    REPORT_FORMAT = os.getenv("REPORT_FORMAT", "json")  # json, html, pdf
    INCLUDE_SCREENSHOTS = os.getenv("INCLUDE_SCREENSHOTS", "false").lower() == "true"
    INCLUDE_TIMELINE = True
    
    # الإشعارات
    NOTIFICATIONS_ENABLED = os.getenv("NOTIFICATIONS_ENABLED", "false").lower() == "true"
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# إنشاء instance من الإعدادات
config = Config()
  
