from dataclasses import dataclass


@dataclass
class ServiceAdmin:
    phone_number: str | None
    email: str | None
