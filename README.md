# Sys-Checker 🔍

A robust Python-based system monitoring tool that proactively watches your server's health and sends beautiful email alerts when resource thresholds are exceeded.

## 🌟 Features

- **Resource Monitoring**: Tracks CPU, RAM, and disk usage in real-time
- **Configurable Alerts**: Set custom thresholds for each resource type
- **Email Notifications**: Professional HTML-formatted alerts via Mailjet
- **System Information**: Comprehensive system details including hostname, uptime, and public IP
- **Logging**: Maintains detailed log files for all alerts and activities
- **Automatic Checks**: Runs on-demand to check system health instantly

## 📋 Requirements

- Python 3.11 or higher
- Internet connection (for email delivery and public IP detection)
- Mailjet account for email notifications

## 🚀 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/shahadil-exthgen/sys-checker.git
   cd sys-checker
   ```

2. **Install dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root with your settings:

   ```env
   # Mailjet credentials
   MJ_APIKEY_PUBLIC=your_public_api_key
   MJ_APIKEY_PRIVATE=your_private_api_key
   SENDER_EMAIL=your-sender@email.com
   RECIPIENT_EMAIL=admin@yourcompany.com

   # System Monitor Thresholds (in percentage)
   CPU_THRESHOLD=80.0
   RAM_THRESHOLD=80.0
   DISK_THRESHOLD=90.0

   # Log file path
   LOG_FILE=system_monitor.log
   ```

## ⚙️ Configuration

### Threshold Settings

- `CPU_THRESHOLD`: CPU usage percentage threshold (default: 80%)
- `RAM_THRESHOLD`: RAM usage percentage threshold (default: 80%)
- `DISK_THRESHOLD`: Disk usage percentage threshold (default: 90%)

### Mailjet Setup

1. Sign up at [Mailjet](https://www.mailjet.com/)
2. Get your API keys from the dashboard
3. Configure sender and recipient email addresses (must be verified in Mailjet)

## 📖 Usage

### Running the Monitor

Simply execute the main script:

```bash
python3 main.py
```

The script will:

1. Check current system resource usage
2. Compare against configured thresholds
3. Send a professional email alert if any thresholds are exceeded
4. Include detailed system information and metrics
5. Log the alert to the specified log file

### Scheduling Regular Checks

For automated monitoring, set up a cron job:

```bash
# Edit crontab
crontab -e

# Add a line to run every 5 minutes
*/5 * * * * cd /path/to/sys-checker && python main.py
```

## 📧 Email Alert Format

When thresholds are exceeded, you'll receive a beautifully formatted HTML email containing:

- **Alert Summary**: Clear indication of which resources are over threshold
- **Live Metrics**: Current CPU, RAM, and disk usage with color-coded indicators
- **System Information**: Hostname, OS details, uptime, and public IP address
- **Timestamp**: When the alert was triggered

## 📝 Logs

All alerts are logged to `system_monitor.log` with timestamps and detailed information. Check this file for historical monitoring data.

## 🔧 Dependencies

- `psutil>=7.1.1`: System resource monitoring
- `mailjet-rest>=1.5.1`: Email delivery service
- `python-dotenv>=1.1.1`: Environment variable management
- `requests>=2.32.5`: HTTP requests for public IP detection

## 👤 Author

Shahadil Exthgen - [GitHub](https://github.com/shahadil-exthgen)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**_Keep your systems healthy and stay informed! 🔔_**
