import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

OUTPUT_DIR = "outputs"
EMAIL_LOG = "logs/email_log.json"

# --- SMTP (Gmail) — load from .env ---
load_dotenv()
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")          # Gmail App Password (no spaces)
DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL", SMTP_USER)



def export_txt(question, answer):
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"answer_{stamp}.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write("QUESTION:\n" + question + "\n\n")
        f.write("ANSWER:\n" + answer + "\n")

    print(f"📄 Text saved → {path}")
    return path

def export_pdf(question, answer):
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"answer_{stamp}.pdf")

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>AI Advisor Response</b>", styles["Title"]),
        Spacer(1, 12),
        Paragraph("<b>Question:</b>", styles["Heading2"]),
        Paragraph(question, styles["Normal"]),
        Spacer(1, 12),
        Paragraph("<b>Answer:</b>", styles["Heading2"]),
        Paragraph(answer.replace("\n", "<br/>"), styles["Normal"]),
    ]
    doc.build(story)

    print(f"📕 PDF saved → {path}")
    return path




def send_email(to_address, subject, body, attachment=None):
    if not to_address or "@" not in to_address or "." not in to_address:
        print(f"⚠️  Invalid recipient '{to_address}' — email skipped.")
        return

    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment and os.path.exists(attachment):
        with open(attachment, "rb") as f:
            data = f.read()
        fname = os.path.basename(attachment)
        subtype = "pdf" if fname.endswith(".pdf") else "plain"
        maintype = "application" if fname.endswith(".pdf") else "text"
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=fname)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email sent → {to_address}")
    except Exception as e:
        print(f"❌ Email failed: {e}")