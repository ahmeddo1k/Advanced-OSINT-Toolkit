import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from rich.console import Console
from .utils import ReportGenerator, InputValidator, Logger

console = Console()
logger = Logger.setup_logger(__name__)

def phone_lookup(number: str) -> dict:
    """
    البحث المتقدم عن أرقام الهواتف
    """
    
    if not InputValidator.is_valid_phone(number):
        console.print("[red]❌ رقم هاتف غير صحيح[/red]")
        return {"error": "Invalid phone number"}
    
    try:
        # محاولة التحليل
        parsed = phonenumbers.parse(number, None)
        
        if not phonenumbers.is_valid_number(parsed):
            console.print("[red]❌ رقم الهاتف غير صحيح[/red]")
            return {"error": "Invalid phone number"}
        
        # استخراج المعلومات
        country_code = parsed.country_code
        national_number = parsed.national_number
        country = geocoder.description_for_number(parsed, "en")
        carrier_name = carrier.name_for_number(parsed, "en")
        timezones = timezone.time_zones_for_number(parsed)
        
        result = {
            "number": number,
            "country": country,
            "country_code": f"+{country_code}",
            "carrier": carrier_name or "Unknown",
            "timezones": list(timezones) if timezones else ["Unknown"],
            "is_valid": True,
            "is_mobile": phonenumbers.number_type(parsed) == phonenumbers.NumberType.MOBILE,
            "formatted": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        }
        
        logger.info(f"Phone lookup successful: {number}")
        return result
        
    except phonenumbers.NumberParseException as e:
        logger.error(f"Phone parse error: {str(e)}")
        return {"error": f"Parse error: {str(e)}"}
    except Exception as e:
        logger.error(f"Phone lookup error: {str(e)}")
        return {"error": f"Lookup error: {str(e)}"}
