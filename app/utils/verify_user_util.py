from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pathlib import Path

from app.core.config import settings
from app.schemas.email_schemas import EmailData, EmailBody

# from app.schemas.email_schema import EmailSchema, EmailVerifySchema
# from fastapi import BackgroundTasks


class Email:
    def __init__(self, background_tasks: BackgroundTasks) -> None:
        self.config = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_SSL_TLS=False,
            MAIL_STARTTLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
        )
        self.bg_tasks = background_tasks

    def send_mail(
        self,
        subject: str,
        recipients: list[str],
        template_body: EmailBody,
        template_name: str,
    ):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            template_body=template_body,
            subtype=MessageType.html,
        )
        mail_instance = FastMail(config=self.config)

        print("Email Sent 1")
        self.bg_tasks.add_task(
            mail_instance.send_message, message, template_name=template_name
        )
        print("Email Sent 2")

    def send_email_verification_mail(self, email: EmailData):
        self.send_mail(
            subject="User Verification",
            recipients=email.model_dump().get("email"),
            template_body=email.model_dump().get("body"),
            template_name="verify_user.html",
        )

    def send_reset_password_mail(self, email: EmailData):
        self.send_mail(
            subject="Password Reset",
            recipients=email.model_dump().get("email"),
            template_body=email.model_dump().get("body"),
            template_name="reset_password.html",
        )
