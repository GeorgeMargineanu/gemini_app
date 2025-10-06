# 🚀 Gemini App — Admin & Deployment Guide

This document explains how to manage, configure, and keep the **Gemini Flask application** running across multiple Google Cloud Shell environments.

---

## 🌍 Google Accounts & Cloud Shell Links

| Account | Description | Cloud Shell URL |
|----------|--------------|-----------------|
| **UMS** | Primary AdReal environment | [Open UMS Cloud Shell](https://5000-cs-513439251914-default.cs-europe-west4-fycr.cloudshell.dev/?authuser=0) |
| **UMS2** | Secondary test environment | [Open UMS2 Cloud Shell](https://5000-cs-1079682634546-default.cs-europe-west4-fycr.cloudshell.dev/?authuser=0) |
| **Tique** | Tique Analytics environment | [Open Tique Cloud Shell](https://5000-cs-770291034213-default.cs-europe-west4-bhnf.cloudshell.dev/?authuser=0) |

---

## 📁 Project Structure

Example folder inside one environment:
```
gemini_app/
├── app.py # Main Flask app
├── flask.log # Log file
├── set_env.sh # Environment variable setup
├── static/ # Static assets (images, JS, CSS)
└── templates/ # HTML templates
```
---

## ⚙️ Environment Setup

Each environment defines its own **environment variables** inside `set_env.sh`.

Example content:

```bash
#!/bin/bash
# Set environment variables for the Gemini app
export PROJECT_LOGO="digital_logo.png"

echo "Environment variables set for this session."
echo "PROJECT_LOGO=$PROJECT_LOGO"
```

To load environment variables, run:
```bash
source set_env.sh
```

# 🧠 Running the Application
To start the Flask app and keep it running in the background:
```bash
# Activate environment variables
source set_env.sh

# Start Flask app and keep it alive
nohup python app.py > flask.log 2>&1 &
```
✅ nohup ensures the app continues running even if the terminal is closed.

# 📜Monitoring Logs

To view live logs:
```bash
tail -f flask.log
```

# 🛑 Stopping the Application
### 1. Find the Flask process:
```bash
ps aux | grep python
```

### 2. Locade the PID for app.py, then stop it:
```bash
kill <PID>
```