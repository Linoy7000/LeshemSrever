from io import BytesIO

import pdfkit
from PIL import Image
from django.http import HttpResponse
# from weasyprint import HTML
from xhtml2pdf import pisa

from simulator.services.display_service import DisplayService
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def render_template_to_html(template_name, context):
    return render_to_string(template_name, context)

def send_email(subject, template_name, context, addressee):
    # Render the template to HTML
    html_message = render_template_to_html(template_name, context)

    # Create the email message
    email = EmailMessage(
        subject,
        html_message,  # Use the HTML message here
        settings.EMAIL_HOST_USER,
        [addressee]
    )

    # Specify that this email is HTML
    email.content_subtype = 'html'

    # Send the email
    email.send(fail_silently=False)

def resize_image(scale, path):
    with Image.open(path) as img:

        img = img.resize((img.width // scale, img.height // scale))
        img.save('C:/Users/לינוי/Downloads/optimized_image.png', optimize=True)


def display_simulation(height, width, elements):
    service = DisplayService(height=height, width=width)
    service.paste_elements(elements)


def get_img_dimensions(path):
    with Image.open(path).convert('RGBA') as img:
        return img.width, img.height

def update_img_dimensions(element):
    w, h = get_img_dimensions(element.get_image_url())
    element.width = w
    element.height = h
    element.save()
