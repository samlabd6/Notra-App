from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv
import os
from pathlib import Path
import random
from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM_EMAIL"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates")
)

mail = FastMail(config=config)


def generate_verification_code():
    return str(random.randint(100000, 999999))

templates = Environment(
    loader=FileSystemLoader(Path(BASE_DIR, "templates")),
    autoescape=select_autoescape(['html', 'xml'])
)

# render the email template with the verification code
def render_template(template_name: str, context: dict):
    template = templates.get_template(template_name)
    return template.render(**context)

# An async function can pause and let other things run while waiting for something to complete, like sending an email. This way, the server can handle other requests instead of being blocked.
async def send_verification_email(recipient: EmailStr, code: str):
    html_content = render_template(
        "verification_email.html",
        {"code": code}
    )

    message = MessageSchema(
        recipients=[recipient],
        subject="Your Email Verification Code",
        html=html_content,
        subtype=MessageType.html
    )

    await mail.send_message(message)




