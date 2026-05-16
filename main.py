import os
import csv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from google import genai

# ReportLab Imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Email/SMTP Imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

app = FastAPI(
    title="SimplifIQ Lead Automation Engine", 
    description="Automated intake, data enrichment, PDF compilation, and outbound delivery network.",
    version="1.0.0"
)

# Configuration Validation Guard
CRITICAL_KEYS = ["GEMINI_API_KEY", "SENDER_EMAIL", "EMAIL_PASSWORD"]
for key in CRITICAL_KEYS:
    if not os.environ.get(key):
        print(f"⚠️ SYSTEM WARNING: Environment variable '{key}' is missing from your session configuration.")

# Initialize Google GenAI client (safely pulls from GEMINI_API_KEY)
client = genai.Client()

# Strict Data Validation Schema
class LeadInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Full name of the lead prospect")
    email: EmailStr = Field(..., description="Valid recipient email address")
    company_name: str = Field(..., min_length=2, description="Name of the corporate entity")
    company_website: str = Field(..., min_length=4, description="Target corporate domain")


def log_to_ledger(name: str, email: str, company: str, pdf_path: str, status: str):
    """
    Appends execution metrics and record tracking details to a local csv ledger.
    Acts as our system data insurance ledger.
    """
    ledger_file = "leads_tracker.csv"
    file_exists = os.path.isfile(ledger_file)
    
    try:
        with open(ledger_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Lead Name", "Email", "Company Name", "Generated PDF File", "Delivery Status"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, email, company, pdf_path, status])
        print(f"📁 Local Ledger updated successfully inside: {ledger_file}")
    except Exception as e:
        print(f"⚠️ Ledger Logging Exception encountered: {e}")


def enrich_company_data(company_name: str, website: str) -> str:
    """Uses Gemini to generate high-value operational insights and challenges."""
    prompt = f"""
    You are an expert business analyst and workflow automation consultant.
    Analyze the following company profile details:
    - Company Name: {company_name}
    - Corporate Domain: {website}

    Generate a highly strategic corporate brief containing:
    1. Core Business Domain, Targeted Market Sector & Expected Value Proposition.
    2. 3 Specific Operational Bottlenecks or inefficiencies standard to this exact business vertical.
    3. Exactly how customized automated workflows (like report creation, CRM syncing, or AI screening) would scale their throughput and capture leaked revenue.

    Tone: Elite, professional, and actionable. Do not use markdown bolding (**) or hashes (#). Use normal paragraphs and line breaks.
    """
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        print(f"🚨 AI Enrichment Failure: {e}")
        # Safe fallback system design choice
        return (f"Operational Feasibility Audit Brief for {company_name}.\n\n"
                f"Due to transient lookup constraints for {website}, our automated platform recommends an immediate "
                f"workflow discovery session focusing on scaling operational outreach and automated report generation models.")


def generate_pdf_report(company_name: str, client_name: str, ai_content: str) -> str:
    """Programmatically builds a polished, publication-ready audit document."""
    clean_name = "".join(x for x in company_name if x.isalnum())
    filename = f"Audit_Report_{clean_name}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    story = []
    styles = getSampleStyleSheet()
    
    PRIMARY_COLOR = colors.HexColor("#1A365D")   # Deep Slate Navy
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") # Modern Indigo Blue
    TEXT_COLOR = colors.HexColor("#2D3748")      # Charcoal Body Text
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=24, leading=28, textColor=PRIMARY_COLOR, spaceAfter=15)
    meta_style = ParagraphStyle('DocMeta', parent=styles['Normal'], fontSize=10, leading=14, textColor=SECONDARY_COLOR, spaceAfter=25)
    body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=11, leading=17, textColor=TEXT_COLOR, spaceAfter=12)

    # Building Flowable Story Elements
    story.append(Paragraph("Automation & AI Feasibility Audit", title_style))
    date_str = datetime.now().strftime("%B %d, %Y")
    meta_text = f"<b>Prepared For:</b> {company_name}<br/><b>Attention:</b> {client_name}<br/><b>Date:</b> {date_str}<br/><b>Origin:</b> SimplifIQ Systems Engineering Framework"
    story.append(Paragraph(meta_text, meta_style))
    
    # Structural Accent Divider Bar
    divider = Table([[""]], colWidths=[504], rowHeights=[3])
    divider.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SECONDARY_COLOR),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(divider)
    story.append(Spacer(1, 20))
    
    # Process text paragraphs safely matching canvas boundaries
    lines = ai_content.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            story.append(Paragraph(line, body_style))
            
    doc.build(story)
    return filename


def send_email_with_attachment(recipient_email: str, recipient_name: str, company_name: str, pdf_filepath: str) -> bool:
    """Establishes security handshake with SMTP gateways to deliver generated assets."""
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    
    if not sender_email or not sender_password:
        print("❌ System skipping transmission protocol: Undefined mail routing variables.")
        return False

    msg = MIMEMultipart()
    msg["From"] = f"SimplifIQ Engineering Automations <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = f"Automated Operational Performance Report | {company_name}"
    
    body = f"""
    <html>
      <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #2D3748; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1A365D; border-bottom: 2px solid #2B6CB0; padding-bottom: 10px;">Executive Feasibility Summary</h2>
        <p>Dear {recipient_name},</p>
        <p>Our automation orchestration pipelines have successfully resolved and parsed background operational metrics regarding <b>{company_name}</b>.</p>
        <p>A comprehensive assessment regarding specific workflow bottlenecks, tech stack vulnerabilities, and AI integrations has been generated for your review.</p>
        <p>Please review the programmatically compiled <b>PDF Document</b> attached to this notification message.</p>
        <br/>
        <p style="font-size: 11px; color: #718096; border-top: 1px solid #E2E8F0; padding-top: 10px;">
          This message was generated dynamically by the SimplifIQ Backend Systems Engine.
        </p>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, "html"))
    
    try:
        with open(pdf_filepath, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_filepath)}")
        msg.attach(part)
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Mailroom Gateway Error: {e}")
        return False


@app.post("/submit-lead/")
async def submit_lead(lead: LeadInput):
    pdf_filename = "Unassigned"
    delivery_status = "Failed"
    try:
        print(f"\n🚀 Processing Pipe Initialized for Lead: {lead.company_name}")
        
        # 1. AI Analysis Call
        ai_insights = enrich_company_data(lead.company_name, lead.company_website)
        
        # 2. PDF Rendering Engine
        pdf_filename = generate_pdf_report(lead.company_name, lead.name, ai_insights)
        
        # 3. SMTP Asset Outbox Dispatch
        email_sent = send_email_with_attachment(lead.email, lead.name, lead.company_name, pdf_filename)
        delivery_status = "Delivered" if email_sent else "SMTP Transmission Error"
        
        # 4. System Tracking Record Logging
        log_to_ledger(lead.name, lead.email, lead.company_name, pdf_filename, delivery_status)
        
        return {
            "status": "success",
            "message": f"Automation processing loop complete for {lead.company_name}.",
            "system_logs": {
                "pdf_compiled": pdf_filename,
                "outbound_delivery": delivery_status,
                "ledger_noted": True
            }
        }
    except Exception as e:
        log_to_ledger(lead.name, lead.email, lead.company_name, pdf_filename, f"System Crash: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline processing crashed: {str(e)}")

@app.get("/")
def home():
    return {"message": "SimplifIQ Pipeline Ecosystem is fully operational."}