import os

from twilio.rest import Client

from wewu_less.models.send_notification_event import SendNotificationEvent

ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
SERVICE_PHONE_NUMBER = "+16303584323"
NOTIFICATION_URL = os.environ["NOTIFICATION_URL"]


class SMSClient:
    client: Client

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_notification(
        self, notification_event: SendNotificationEvent, phone_number: str
    ):
        ack_url = (
            f"{NOTIFICATION_URL}?notificationId={notification_event.notification_id}"
        )
        message_body = (
            f"Fail for job {notification_event.job_id} detected.\n ACK: {ack_url}"
        )

        self.client.messages.create(
            from_=SERVICE_PHONE_NUMBER, to=phone_number, body=message_body
        )
