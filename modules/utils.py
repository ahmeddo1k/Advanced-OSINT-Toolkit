import logging
import json
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing import Dict, Any, List, Optional
import re
import hashlib
import requests
import time
from config import (
    SHODAN_API_KEY, VIRUSTOTAL_API_KEY, REQUEST_TIMEOUT,
    REPORTS_DIR, RATE_LIMIT_DELAY
)

console = Console()
logger = logging.getLogger(__name__)

class ReportGenerator:
    """توليد التقارير بصيغ مختلفة"""
    
    def __init__(self, report_type: str = "txt"):
        self.report_type = report_type
        self.data = {}
        self.timestamp = datetime.now()
    
    def add_section(self, title: str, content: Dict[str, Any]):
        """إضافة قسم للتقرير"""
        self.data[title] = content
    
    def generate_txt(self) -> str:
        """توليد تقرير نصي منسق"""
        report = f"""
╔════════════════════════════════════════╗
║   Advanced OSINT Toolkit Report        ║
╚════════════════════════════════════════╝

Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

"""
        for section_title, content in self.data.items():
            report += f"\n{'='*40}\n{section_title}\n{'='*40}\n"
            
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, list):
                        report += f"{key}:\n"
                        for item in value:
                            report += f"  • {item}\n"
                    else:
                        report += f"{key}: {value}\n"
            elif isinstance(content, list):
                for item in content:
                    report += f"  • {item}\n"
            else:
                report += str(content) + "\n"
        
        return report
    
    def generate_json(self) -> str:
        """توليد تقرير JSON"""
        report = {
            "metadata": {
                "generated": self.timestamp.isoformat(),
                "tool": "Advanced OSINT Toolkit"
            },
            "data": self.data
        }
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def generate_html(self) -> str:
        """توليد تقرير HTML"""
        html = f"""<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>OSINT Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 20px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .section {{ margin: 20px 0; }}
        .section h2 {{ color: #007bff; margin-top: 20px; }}
        .info-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }}
        .label {{ font-weight: bold; color: #555; }}
        .value {{ color: #333; }}
        .timestamp {{ color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Advanced OSINT Toolkit Report</h1>
        <p class="timestamp">Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
        for section_title, content in self.data.items():
            html += f'<div class="section"><h2>{section_title}</h2>'
            
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, list):
                        html += f'<div class="info-row"><span class="label">{key}</span><span class="value">{", ".join(str(v) for v in value)}</span></div>'
                    else:
                        html += f'<div class="info-row"><span class="label">{key}</span><span class="value">{value}</span></div>'
            
            html += '</div>'
        
        html += '</body></html>'
        return html
    
    def save(self, filename: str) -> str:
        """حفظ التقرير"""
        Path(REPORTS_DIR).mkdir(exist_ok=True)
        
        if self.report_type == "json":
            content = self.generate_json()
            filepath = f"{REPORTS_DIR}/{filename}.json"
        elif self.report_type == "html":
            content = self.generate_html()
            filepath = f"{REPORTS_DIR}/{filename}.html"
        else:
            content = self.generate_txt()
            filepath = f"{REPORTS_DIR}/{filename}.txt"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath

class InputValidator:
    """التحقق من صحة المدخلات"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        phone = re.sub(r'\D', '', phone)
        return len(phone) >= 10
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return re.match(pattern, domain) is not None
    
    @staticmethod
    def is_valid_username(username: str) -> bool:
        return 3 <= len(username) <= 30 and re.match(r'^[a-zA-Z0-9_.-]+$', username)

class Logger:
    """نظام تسجيل متقدم"""
    
    @staticmethod
    def setup_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        
        Path("logs").mkdir(exist_ok=True)
        
        handler = logging.FileHandler(f"logs/{datetime.now().strftime('%Y%m%d')}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        return logger

def display_table(title: str, data: Dict[str, Any]):
    """عرض جدول منسق"""
    table = Table(title=title)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in data.items():
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        table.add_row(str(key), str(value))
    
    console.print(table)

def hash_data(data: str) -> str:
    """حساب hash للبيانات"""
    return hashlib.sha256(data.encode()).hexdigest()

class APIManager:
    """إدارة استدعاءات API مع احترام حدود المعدل"""
    
    def __init__(self):
        self.last_request_time = 0
    
    def rate_limit(self):
        """تطبيق تأخير بين الطلبات"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        self.last_request_time = time.time()
    
    def shodan_lookup(self, ip: str) -> Optional[Dict]:
        """استعلام Shodan عن IP"""
        if not SHODAN_API_KEY:
            return {"error": "Shodan API key not configured"}
        
        self.rate_limit()
        try:
            import shodan
            api = shodan.Shodan(SHODAN_API_KEY)
            host = api.host(ip)
            return {
                "ip": host.get("ip_str"),
                "organization": host.get("org", "N/A"),
                "os": host.get("os", "N/A"),
                "ports": host.get("ports", []),
                "vulns": list(host.get("vulns", []))[:5],  # أول 5 ثغرات
                "country": host.get("country_name", "N/A"),
                "city": host.get("city", "N/A")
            }
        except Exception as e:
            logger.error(f"Shodan error: {e}")
            return {"error": str(e)}
    
    def virustotal_domain_report(self, domain: str) -> Optional[Dict]:
        """استعلام VirusTotal عن المجال"""
        if not VIRUSTOTAL_API_KEY:
            return {"error": "VirusTotal API key not configured"}
        
        self.rate_limit()
        try:
            url = f"https://www.virustotal.com/api/v3/domains/{domain}"
            headers = {"x-apikey": VIRUSTOTAL_API_KEY}
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                attrs = data.get("data", {}).get("attributes", {})
                stats = attrs.get("last_analysis_stats", {})
                return {
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "undetected": stats.get("undetected", 0),
                    "reputation": attrs.get("reputation", 0),
                    "categories": ", ".join(attrs.get("categories", {}).values())
                }
            return {"error": f"Status {response.status_code}"}
        except Exception as e:
            logger.error(f"VirusTotal error: {e}")
            return {"error": str(e)}
