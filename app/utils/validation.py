from fastapi import BackgroundTasks

from app.models.user_model import User
from app.schemas import email_schemas
from app.utils.verify_user_util import Email


def email_vaildation(
    background_tasks: BackgroundTasks, new_user: User, access_token: str
):
    email_verification_data = email_schemas.EmailData(
        email=[new_user.email],
        body=email_schemas.EmailBody(
            token=access_token,
            username=new_user.username,
        ),
    )
    verification_email = Email(background_tasks=background_tasks)

    background_tasks.add_task(
        verification_email.send_email_verification_mail,
        email=email_verification_data,
    )
