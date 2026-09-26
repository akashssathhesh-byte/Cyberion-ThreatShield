# Cyberion-ThreatShield
It is a defensive cybersecurity monitoring and threat-detection system designed for security labs, SOC internships, and portfolio projects.
It monitors selected directories for suspicious file activity, calculates file hashes, applies configurable detection rules, records security events, and exposes a lightweight dashboard/API for reviewing alerts.Cyberion Shield is intended for authorized systems, security labs, and incident-response practice.

Features

- Real-time filesystem monitoring
- SHA-256 file hashing
- Suspicious extension detection
- Rapid file-activity detection
- Alert severity classification
- JSONL security-event logging
- YAML configuration
- SQLite alert database
- FastAPI REST API
- Simple HTML dashboard
- IOC/hash lookup endpoint
- Modular architecture suitable for future SIEM/SOC integration

Architecture

```text
              ┌─────────────────────┐
              │   Monitored Folder  │
              └──────────┬──────────┘
                         │ file events
                         ▼
              ┌─────────────────────┐
              │  File Event Watcher │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │ Detection Engine    │
              │ • extension rules   │
              │ • activity rules    │
              │ • hash generation   │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │ Alert Manager       │
              │ severity + metadata │
              └───────┬───────┬─────┘
                      │       │
                ┌─────▼──┐ ┌─▼────────┐
                │ SQLite │ │ JSONL Log │
                └─────┬──┘ └────┬──────┘
                      └──────┬───┘
                             ▼
                    ┌────────────────┐
                    │ FastAPI / UI   │
                    └────────────────┘
```

Project Structure
```text
Cyberion-Shield/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── detector.py
│   ├── logger.py
│   ├── models.py
│   ├── watcher.py
│   └── main.py
├── dashboard/
│   └── index.html
├── config.yaml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```
Installation

1. Clone the repository

```bash
git clone https://github.com/<your-username>/Cyberion-Shield.git
cd Cyberion-Shield
```

2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure the project

Edit `config.yaml` and change `monitor_path` to a directory you are authorized to monitor.

5. Start the API/dashboard

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Dashboard |
| `/health` | GET | Health check |
| `/alerts` | GET | Recent alerts |
| `/stats` | GET | Alert statistics |
| `/ioc/{sha256}` | GET | Search an observed SHA-256 |

Example:

```bash
curl http://127.0.0.1:8000/health
```

Detection Logic

Cyberion Shield currently detects:

1. **Suspicious extensions** configured in `config.yaml`.
2. **High-volume file activity** within a configurable time window.
3. **Large file changes** above the configured size threshold.
4. SHA-256 hashes for observed files.
5. Alert severity based on the triggered rule.

This is a behavioral detection prototype, not a replacement for a commercial EDR/antivirus product.

Example Alert

```json
{
  "severity": "HIGH",
  "rule": "SUSPICIOUS_EXTENSION",
  "path": "/lab/sample.suspicious",
  "sha256": "example",
  "message": "A configured suspicious file extension was observed."
}
```

GitHub Upload

```bash
git init
git add .
git commit -m "Initial Cyberion Shield project"
git branch -M main
git remote add origin https://github.com/<your-username>/Cyberion-Shield.git
git push -u origin main
```

Future Enhancements

- YARA integration
- VirusTotal integration using an API key
- MITRE ATT&CK mapping
- Email/Telegram/Slack alerting
- Wazuh/Splunk forwarding
- Windows Event Log monitoring
- Process monitoring
- Quarantine workflow with explicit analyst approval
- Authentication and role-based access
- Docker deployment
- Automated unit/integration tests
