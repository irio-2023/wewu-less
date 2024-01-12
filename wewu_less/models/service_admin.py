from dataclasses import dataclass


@dataclass
class ServiceAdmin:
    phone_number: str | None = None
    email: str | None = None
