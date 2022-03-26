from rest_framework.response import Response
import re


def validate_keys(payload, required_keys):
    """Validate if there is any missing required keys."""
    # extract keys from payload
    payload_keys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missing_keys = []
    for key in required_keys:
        if key not in payload_keys:
            missing_keys.append(key)

    return missing_keys


def validate_empty_str(value):
    """Validate if the String is empty."""
    return len(value.strip()) > 0


def http_response(msg, status, data=None, error_code=None):
    """Custom API Response."""
    if data is None:
        data = {}

    success = True
    response_data = dict(
        success=success,
        message=msg,
        data=data,
    )
    if error_code:
        success = False
        response_data['success'] = success
        response_data['error_code'] = error_code

    return Response(response_data, status=status)


def validate_email_format(email):
    """Validate email pattern."""
    email_pattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'

    if re.search(email_pattern, email):
        return True
    return False
