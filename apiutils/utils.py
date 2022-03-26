from django.apps import apps as django_apps
import random
import string
import logging

logger = logging.getLogger(__name__)


def generate_code(app_label, model_name):
    """Generate Unique Code For Model."""
    try:
        # length of the code
        length = 14

        # get model through the app name
        model = django_apps.get_model(app_label, model_name)

        # ascii combination of letters and numbers
        ascii_values = string.ascii_letters + string.digits

        while True:
            code = ''.join(random.choices(ascii_values, k=length))
            if model.objects.filter(code=code).exists():
                # if True i.e if code exist, generate another code
                generate_code(app_label, model_name)

            else:
                # if False i.e if code does not exist, stop.
                break
        return f'{code}'

    except Exception as e:
        logger.error('generate_code@Error')
        logger.error(e)
        return None