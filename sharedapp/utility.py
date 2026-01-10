import re
from rest_framework.validators import ValidationError

email_regex = re.compile(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")
phone_regex = re.compile(r"^(?:\+?998[\s-]?)?(?:(?:(?:9[01345789]|88)\s?\d{2}|71\s?\d{2})[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})$")

def email_or_phone_number(email_or_phone_number):
    if re.fullmatch(email_regex, email_or_phone_number):
        email_or_phone = 'email'

    elif re.fullmatch(phone_regex, email_or_phone_number):
        email_or_phone = 'phone'
        
    else:
        data = {
            'success': 'False',
            'message': 'phone or email has been entered wrongly'
        }

        raise ValidationError(data)
    
    return email_or_phone