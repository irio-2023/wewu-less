from marshmallow import Schema, ValidationError, fields, validates, validates_schema


class ServiceAdminSchema(Schema):
    email = fields.Email(allow_none=True)
    phone_number = fields.String(data_key="phoneNumber", allow_none=True)

    @validates_schema
    def validate_only_one_contact_method(self, data, **kwargs):
        if (
            data.get("email", None) is not None
            and data.get("phone_number", None) is not None
        ):
            raise ValidationError("Only one contact method is permitted")
        if data.get("email", None) is None and data.get("phone_number", None) is None:
            raise ValidationError("At least one contact method is required")

    @validates("phone_number")
    def validate_phone_number(self, phone_number: str | None):
        is_valid = True
        if phone_number is not None:
            is_valid = (
                9 <= len(phone_number) <= 12
                and all([c.isdigit() for c in phone_number[1:]])
                and (phone_number[0].isdigit() or phone_number[0] == "+")
            )

        if not is_valid:
            raise ValidationError(
                "Invalid phone number, it should consist of 9 digits",
                field_name="phone_number",
            )
