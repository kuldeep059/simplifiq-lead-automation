# SimplifIQ - AI Software Developer Intern Automation Engine

A robust, enterprise-grade automation microservice built with **FastAPI** and **Python 3**. This system automates the entire lead intake and follow-up pipeline: validating inbound leads, generating domain-specific business intelligence insights via the **Google Gemini API**, programmatically drawing stylized corporate audit PDFs using **ReportLab**, dispatching secure HTML asset notifications via **SMTP**, and ensuring data persistence with an execution ledger.

---

## 🏗️ System Architecture & Workflow

The backend follows a sequential pipeline design where each phase acts as an automated assembly node:

1. **Intake API Gate (`FastAPI` + `Pydantic`):** Exposes a clean `POST` endpoint that handles rigorous schema typing, structure filtering, and email validation strings using `EmailStr` before allowing any downstream execution.
2. **AI Enrichment Framework (`Google GenAI`):** Leverages the state-of-the-art `gemini-2.5-flash` model to analyze the lead's domain and construct customized executive summaries, target sector opportunities, and technical workflow solutions.
3. **Asset Compilation Layer (`ReportLab`):** Dynamically builds corporate-branded PDF documents. It programmatically formats canvas boundaries, paragraph spacing, and geometric dividers to guarantee a clean, professional aesthetic.
4. **Outbound Notification Agent (`smtplib`):** Coordinates secure TLS-wrapped authentication handshakes with email gateways to dispatch dynamic, responsive HTML envelopes directly to the prospect's inbox with the PDF safely attached.
5. **Operational Ledger Sync (`CSV Tracker`):** Acts as a local transactional ledger. It maps execution timestamps, path locations, user context, and delivery statuses to ensure strict data observability.

---

## ⚙️ Quickstart & Environment Initialization

Follow these steps to initialize and run the automation engine locally:

### 1. Project Directory & Environment Setup
Clone or create your project directory, create an isolated virtual environment, and activate it:
```powershell
# Create project folder
cd D:\simplifiq-automation

# Initialize Python Virtual Environment
python -m venv venv

# Activate Environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
---

### 2. Install Project Dependencies
Ensure your virtual environment is active (indicated by (venv) in your terminal prompt) and execute:

```powershell
pip install fastapi uvicorn google-genai pydantic reportlab email-validator

### 3. Configure Secure Environment Secrets
Inject your API credentials directly into your active terminal session. This keeps production secrets abstracted entirely out of the source code codebase:

```powershell
$env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
$env:SENDER_EMAIL="your_gmail_account@gmail.com"
$env:EMAIL_PASSWORD="your_16_character_gmail_app_password"

### 4. Launch the Gateway Development Server



If want demo link follow me here 

```powershell
uvicorn main:app --reload
---
Once the server is live, navigate to the auto-generated interactive testing lab at:

👉 http://127.0.0.1:8000/docs
