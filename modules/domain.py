import whois

def domain_lookup(domain):

    try:
        data = whois.whois(domain)

        return f"""
DOMAIN REPORT
Domain: {domain}
Registrar: {data.registrar}
Creation Date: {data.creation_date}
Expiration Date: {data.expiration_date}
Name Servers: {data.name_servers}
"""

    except:
        return "Could not fetch domain data"
