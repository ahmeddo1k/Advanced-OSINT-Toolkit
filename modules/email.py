import re
from typing import Dict, Any
from .utils import InputValidator, Logger
from rich.console import Console

console = Console()
logger = Logger.setup_logger(__name__)

class EmailAnalyzer:
    """محلل متقدم للبريد الإلكتروني"""
    
    # قائمة الخوادم الشهيرة
    POPULAR_PROVIDERS = {
        "gmail.com": "Google",
        "yahoo.com": "Yahoo",
        "outlook.com": "Microsoft",
        "hotmail.com": "Microsoft",
        "protonmail.com": "ProtonMail",
        "tutanota.com": "Tutanota",
        "icloud.com": "Apple",
        "aol.com": "AOL",
        "yandex.com": "Yandex"
    }
    
    @staticmethod
    def analyze(email: str) -> Dict[str, Any]:
        """تحليل البريد الإلكتروني"""
        
        if not InputValidator.is_valid_email(email):
            console.print("[red]❌ صيغة البريد الإلكتروني غير صحيحة[/red]")
            return {"error": "Invalid email format"}
        
        try:
            username, domain = email.split("@", 1)
            
            provider = EmailAnalyzer.POPULAR_PROVIDERS.get(domain, "Unknown")
            
            # فحص الأمان
            is_secure = domain in EmailAnalyzer.POPULAR_PROVIDERS
            
            result = {
                "email": email,
                "username": username,
                "domain": domain,
                "provider": provider,
                "is_secured": is_secure,
                "format_valid": True,
                "username_length": len(username),
                "domain_length": len(domain)
            }
            
            logger.info(f"Email analyzed: {email}")
            return result
            
        except Exception as e:
            logger.error(f"Email analysis error: {str(e)}")
            return {"error": f"Analysis error: {str(e)}"}

def email_lookup(email: str) -> dict:
    """دالة البحث الرئيسية"""
    analyzer = EmailAnalyzer()
    return analyzer.analyze(email)
