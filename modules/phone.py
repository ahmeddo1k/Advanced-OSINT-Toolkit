import phonenumbers
from phonenumbers import geocoder, carrier

def phone_lookup(number):

    try:
        parsed = phonenumbers.parse(number)

        country = geocoder.description_for_number(parsed, "en")
        sim = carrier.name_for_number(parsed, "en")

        return f"""
PHONE REPORT
Number: {number}
Country: {country}
Carrier: {sim}
Valid: {phonenumbers.is_valid_number(parsed)}
"""

    except:
        return "Invalid phone number"
