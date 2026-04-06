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
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates")
)


def generate_verification_token():
    return str(random.randint(100000, 999999))





mail = FastMail(config=config)

def create_message(recipient:EmailStr, subject:str, body : str):
    message = MessageSchema(
        recipients=[recipient],
        subject=subject,
        body=body, 
        subtype=MessageType.html
    ) 
    return message 
