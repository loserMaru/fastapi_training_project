from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException


def email_validation(email):
    try:
        email = validate_email(email, check_deliverability=False)
        email = email.normalized
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return email