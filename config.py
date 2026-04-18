import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")

# Timeout Settings
REQUEST_TIMEOUT = 10
WHOIS_TIMEOUT = 15

# Report Settings
REPORT_FORMAT = "json"  # json, txt, html
REPORTS_DIR = "reports"
LOGS_DIR = "logs"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Rate Limiting
RATE_LIMIT_DELAY = 1  # seconds between requests

# Validation
VALIDATE_INPUTS = True
MAX_INPUT_LENGTH = 500
