import psutil
import logging
import platform
import socket
import os
from datetime import datetime, timedelta
from mailjet_rest import Client
import requests
from config import MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE, SENDER_EMAIL, RECIPIENT_EMAIL

# ----------------- CONFIG -----------------
# Thresholds
CPU_THRESHOLD = 80.0  # %
RAM_THRESHOLD = 80.0  # %
DISK_THRESHOLD = 90.0  # %

# Log file
LOG_FILE = "system_monitor.log"

# ----------------------------------------

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Mailjet client
mailjet = Client(
    auth=(
        MJ_APIKEY_PUBLIC,
        MJ_APIKEY_PRIVATE,
    ),
    version="v3.1",
)

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Unable to fetch public IP"
    except Exception as e:
        return f"Error fetching public IP: {e}"

def get_system_info():
    uname = platform.uname()
    hostname = socket.gethostname()
    uptime_seconds = float(os.popen("cat /proc/uptime").readline().split()[0])
    uptime_string = str(timedelta(seconds=int(uptime_seconds)))
    
    public_ip = get_public_ip()
    
    sys_info = {
        'hostname': hostname,
        'system': uname.system,
        'node_name': uname.node,
        'release': uname.release,
        'version': uname.version,
        'machine': uname.machine,
        'processor': uname.processor,
        'uptime': uptime_string,
        'public_ip': public_ip
    }
    return sys_info

def create_html_email(alerts, system_info, metrics):
    """Create a beautiful HTML email body"""
    
    # Alert rows HTML
    alert_rows = ""
    for alert in alerts:
        alert_rows += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #fee; background-color: #fff5f5;">
                <span style="color: #c53030; font-weight: 500;">⚠️ {alert}</span>
            </td>
        </tr>
        """
    
    # System info rows
    info_rows = ""
    info_labels = {
        'hostname': 'Hostname',
        'system': 'System',
        'node_name': 'Node Name',
        'release': 'Release',
        'machine': 'Machine',
        'processor': 'Processor',
        'uptime': 'Uptime',
        'public_ip': 'Public IP'
    }
    
    for key, label in info_labels.items():
        info_rows += f"""
        <tr>
            <td style="padding: 10px 15px; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #4a5568; width: 150px;">{label}</td>
            <td style="padding: 10px 15px; border-bottom: 1px solid #e2e8f0; color: #2d3748;">{system_info.get(key, 'N/A')}</td>
        </tr>
        """
    
    # Metric cards
    cpu_color = "#ef4444" if metrics['cpu'] > CPU_THRESHOLD else "#10b981"
    ram_color = "#ef4444" if metrics['ram'] > RAM_THRESHOLD else "#10b981"
    disk_color = "#ef4444" if metrics['disk'] > DISK_THRESHOLD else "#10b981"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f7fafc;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f7fafc; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700;">🚨 System Alert</h1>
                                <p style="margin: 10px 0 0 0; color: #e6e6ff; font-size: 14px;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                            </td>
                        </tr>
                        
                        <!-- Alerts Section -->
                        <tr>
                            <td style="padding: 30px;">
                                <h2 style="margin: 0 0 20px 0; color: #c53030; font-size: 20px; font-weight: 600;">⚠️ Critical Alerts</h2>
                                <table width="100%" cellpadding="0" cellspacing="0" style="border: 2px solid #fc8181; border-radius: 6px; overflow: hidden;">
                                    {alert_rows}
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Metrics Section -->
                        <tr>
                            <td style="padding: 0 30px 30px 30px;">
                                <h2 style="margin: 0 0 20px 0; color: #2d3748; font-size: 20px; font-weight: 600;">📊 Current Metrics</h2>
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="padding: 0 5px 15px 0; width: 33.33%;">
                                            <div style="background-color: #f7fafc; border-left: 4px solid {cpu_color}; padding: 15px; border-radius: 4px;">
                                                <div style="color: #718096; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px;">CPU Usage</div>
                                                <div style="color: #2d3748; font-size: 24px; font-weight: 700;">{metrics['cpu']}%</div>
                                            </div>
                                        </td>
                                        <td style="padding: 0 5px 15px 5px; width: 33.33%;">
                                            <div style="background-color: #f7fafc; border-left: 4px solid {ram_color}; padding: 15px; border-radius: 4px;">
                                                <div style="color: #718096; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px;">RAM Usage</div>
                                                <div style="color: #2d3748; font-size: 24px; font-weight: 700;">{metrics['ram']}%</div>
                                            </div>
                                        </td>
                                        <td style="padding: 0 0 15px 5px; width: 33.33%;">
                                            <div style="background-color: #f7fafc; border-left: 4px solid {disk_color}; padding: 15px; border-radius: 4px;">
                                                <div style="color: #718096; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px;">Disk Usage</div>
                                                <div style="color: #2d3748; font-size: 24px; font-weight: 700;">{metrics['disk']}%</div>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- System Info Section -->
                        <tr>
                            <td style="padding: 0 30px 30px 30px;">
                                <h2 style="margin: 0 0 20px 0; color: #2d3748; font-size: 20px; font-weight: 600;">💻 System Information</h2>
                                <table width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
                                    {info_rows}
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f7fafc; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                                <p style="margin: 0; color: #718096; font-size: 12px;">
                                    This is an automated alert from your System Monitor<br>
                                    Please take appropriate action to resolve the issues
                                </p>
                            </td>
                        </tr>
                        
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return html

def send_email(subject, text_body, html_body=None):
    """Send email using Mailjet"""
    if not SENDER_EMAIL or not RECIPIENT_EMAIL:
        print("⚠️ SENDER_EMAIL or RECIPIENT_EMAIL not configured in environment.")
        return

    if html_body is None:
        html_body = f"<pre>{text_body}</pre>"

    data = {
        "Messages": [
            {
                "From": {"Email": SENDER_EMAIL, "Name": "System Monitor"},
                "To": [{"Email": RECIPIENT_EMAIL, "Name": "Admin"}],
                "Subject": subject,
                "TextPart": text_body,
                "HTMLPart": html_body,
            }
        ]
    }

    try:
        response = mailjet.send.create(data=data)
        print(f"📧 Email status: {response.status_code}")
        try:
            response_json = response.json()
            if response.status_code != 200:
                print(f"❌ Email send error: {response_json}")
                logging.error(f"Failed to send email: {response_json}")
            else:
                logging.info("Alert email sent successfully.")
        except Exception as json_error:
            print(f"❌ Failed to parse Mailjet response: {json_error}")
            logging.error(f"Failed to parse Mailjet response: {json_error}")
    except Exception as e:
        print(f"❌ Exception while sending email: {e}")
        logging.error(f"Exception while sending email: {e}")

def check_metrics():
    alerts = []
    
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > CPU_THRESHOLD:
        alerts.append(f"High CPU usage detected: {cpu_percent}%")
    
    ram_percent = psutil.virtual_memory().percent
    if ram_percent > RAM_THRESHOLD:
        alerts.append(f"High RAM usage detected: {ram_percent}%")
    
    disk_percent = psutil.disk_usage('/').percent
    if disk_percent > DISK_THRESHOLD:
        alerts.append(f"High Disk usage detected: {disk_percent}%")
    
    metrics = {
        'cpu': cpu_percent,
        'ram': ram_percent,
        'disk': disk_percent
    }
    
    return alerts, metrics

def main():
    alerts, metrics = check_metrics()
    if alerts:
        system_info = get_system_info()
        
        # Create plain text version for TextPart
        text_body = "\n".join(alerts) + "\n\nSystem Info:\n"
        for key, value in system_info.items():
            text_body += f"{key.replace('_', ' ').title()}: {value}\n"
        
        # Log the alert
        logging.warning(text_body)
        
        # Create HTML email body
        html_body = create_html_email(alerts, system_info, metrics)
        
        # Send email
        send_email("🚨 System Resource Alert!", text_body, html_body)
    else:
        print("✅ All metrics are within limits.")

if __name__ == "__main__":
    main()