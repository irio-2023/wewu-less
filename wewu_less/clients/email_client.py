import os

from mailjet_rest import Client

from wewu_less.logging import get_logger
from wewu_less.models.send_notification_event import SendNotificationEvent

logger = get_logger()

notification_url = os.environ["NOTIFICATION_URL"]
service_mail = os.environ["SERVICE_MAIL"]
mail_api_key = os.environ["MAIL_API_KEY"]
mail_api_secret = os.environ["MAIL_API_SECRET"]

default_client = Client(auth=(mail_api_key, mail_api_secret))


class EmailClient:
    def __init__(self, mailjet_client=default_client):
        self.mailjet_client = mailjet_client

    def send_notification(
        self,
        notification_event: SendNotificationEvent,
        email: str,
        from_email=service_mail,
    ):
        url = f"{notification_url}?notificationId={notification_event.notification_id}"
        body = f"Fail for job {notification_event.job_id} detected.\n ACK: {url}"
        self.send_email(
            from_email=from_email,
            from_name="Wewu Alerter",
            to_email=email,
            subject="[WEWU] Service fail detected",
            text=body,
        )

    def send_email(self, from_name, from_email, to_email, subject, text):
        try:
            data = {
                "FromEmail": from_email,
                "FromName": from_name,
                "Subject": subject,
                "Text-part": text,
                "Recipients": [{"Email": to_email}],
            }
            result = self.mailjet_client.send.create(data=data)
            if result.status_code != 200:
                raise Exception(result.status_code, result.text)
        except Exception:
            logger.exception("Failed to send mail", mail=to_email)
            raise
