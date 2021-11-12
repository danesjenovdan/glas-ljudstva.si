import string
import random
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


from django.template.loader import render_to_string


from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def send_email(subject, to_email, template, data, from_email=settings.FROM_EMAIL):
    html_body = render_to_string(template, data)
    text_body = strip_tags(html_body)

    (
        subject=subject,
        from_email=from_email,
        to=[to_efrom_emailfrom_emailmail],
        body=text_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
