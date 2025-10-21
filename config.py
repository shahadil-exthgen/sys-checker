import os
from dotenv import load_dotenv

load_dotenv()

# Mailjet credentials
MJ_APIKEY_PUBLIC = os.getenv("MJ_APIKEY_PUBLIC")
MJ_APIKEY_PRIVATE = os.getenv("MJ_APIKEY_PRIVATE")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# System Monitor Thresholds
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "80.0"))
RAM_THRESHOLD = float(os.getenv("RAM_THRESHOLD", "80.0"))
DISK_THRESHOLD = float(os.getenv("DISK_THRESHOLD", "90.0"))

# Log file
LOG_FILE = os.getenv("LOG_FILE", "system_monitor.log")