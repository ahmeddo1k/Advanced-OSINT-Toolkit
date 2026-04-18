import whois
import dns.resolver
import dns.rdatatype
from typing import Dict, Any, List, Optional
from .utils import Logger, APIManager
from rich.console import Console
import socket
import ssl
import OpenSSL
import requests
from datetime import datetime
import tldextract

console = Console()
logger = Logger.setup_logger(__name__)
api_manager = APIManager()

class DomainAnalyzer:
    """محلل متقدم للمجالات"""
    
    @staticmethod
    def get_whois_info(domain: str) -> Dict[str, Any]:
        """الحصول على معلومات WHOIS"""
        try:
            data = whois.whois(domain)
            
            # التعامل مع التواريخ المتعددة
            creation = data.creation_date
            if isinstance(creation, list):
                creation = creation[0]
            expiration = data.expiration_date
            if isinstance(expiration, list):
                expiration = expiration[0]
            
            return {
                "registrar": str(data.registrar) if data.registrar else "Unknown",
                "creation_date": str(creation) if creation else "Unknown",
                "expiration_date": str(expiration) if expiration else "Unknown",
                "name_servers": data.name_servers if data.name_servers else [],
                "status": data.status if data.status else [],
                "registrant": str(data.registrant) if hasattr(data, 'registrant') else "Private",
                "emails": data.emails if hasattr(data, 'emails') else []
            }
        except Exception as e:
            logger.error(f"WHOIS lookup error for {domain}: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def get_dns_records(domain: str) -> Dict[str, List[str]]:
        """الحصول على سجلات DNS"""
        dns_records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type, raise_on_no_answer=False)
                dns_records[record_type] = [str(rdata) for rdata in answers]
            except Exception as e:
                logger.debug(f"DNS {record_type} lookup failed for {domain}: {str(e)}")
                dns_records[record_type] = []
        
        return dns_records
    
    @staticmethod
    def get_ip_address(domain: str) -> str:
        """الحصول على عنوان IP"""
        try:
            return socket.gethostbyname(domain)
        except Exception as e:
            logger.error(f"IP lookup error for {domain}: {str(e)}")
            return "Unknown"
    
    @staticmethod
    def get_ssl_info(domain: str) -> Dict[str, Any]:
        """الحصول على معلومات شهادة SSL"""
        try:
            cert = ssl.get_server_certificate((domain, 443))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            
            subject = dict(x509.get_subject().get_components())
            issuer = dict(x509.get_issuer().get_components())
            
            not_after = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
            not_before = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
            
            return {
                "subject": {k.decode(): v.decode() for k, v in subject.items()},
                "issuer": {k.decode(): v.decode() for k, v in issuer.items()},
                "not_before": not_before.isoformat(),
                "not_after": not_after.isoformat(),
                "expired": datetime.now() > not_after,
                "serial_number": str(x509.get_serial_number()),
                "version": x509.get_version()
            }
        except Exception as e:
            logger.error(f"SSL info error for {domain}: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def get_subdomains(domain: str) -> List[str]:
        """استخراج النطاقات الفرعية من crt.sh"""
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    for sub in name.split('\n'):
                        if sub.endswith(f".{domain}"):
                            subdomains.add(sub.strip())
            return list(subdomains)[:50]  # تحديد أول 50
        except Exception as e:
            logger.error(f"Subdomain enumeration error: {e}")
            return []
    
    @staticmethod
    def analyze(domain: str) -> Dict[str, Any]:
        """تحليل شامل للمجال"""
        
        # تنظيف المدخل
        ext = tldextract.extract(domain)
        clean_domain = f"{ext.domain}.{ext.suffix}"
        
        console.print(f"[bold cyan]🔍 Analyzing domain: {clean_domain}[/bold cyan]")
        
        result = {
            "domain": clean_domain,
            "ip": DomainAnalyzer.get_ip_address(clean_domain),
            "whois": DomainAnalyzer.get_whois_info(clean_domain),
            "dns": DomainAnalyzer.get_dns_records(clean_domain),
            "ssl": DomainAnalyzer.get_ssl_info(clean_domain),
            "subdomains": DomainAnalyzer.get_subdomains(clean_domain),
            "shodan": {},
            "virustotal": {}
        }
        
        # إضافة Shodan إذا توفر IP
        if result["ip"] and result["ip"] != "Unknown":
            result["shodan"] = api_manager.shodan_lookup(result["ip"])
        
        # إضافة VirusTotal
        result["virustotal"] = api_manager.virustotal_domain_report(clean_domain)
        
        logger.info(f"Domain analysis completed for {clean_domain}")
        return result

def domain_lookup(domain: str) -> dict:
    """دالة البحث الرئيسية عن المجال"""
    analyzer = DomainAnalyzer()
    return analyzer.analyze(domain)
