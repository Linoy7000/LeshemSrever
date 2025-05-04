import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from server.services.email_service import EmailService


class UploadImage(APIView):
    def post(self, request, folder):
        try:
            if request.method == 'POST' and request.FILES['image']:
                image = request.FILES['image']
                file_extension = os.path.splitext(image.name)[1]
                new_filename = get_random_string(10) + file_extension
                save_dir = os.path.join(settings.MEDIA_ROOT, folder)
                fs = FileSystemStorage(location=save_dir)
                filename = fs.save(new_filename, image)
                return Response({'image_url': os.path.splitext(filename)[0]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'err': "Error"}, status=status.HTTP_400_BAD_REQUEST)


class EmailView(APIView):
    def post(self, request):

        try:
            receipts = request.POST.get('receipts').split(",")
            subject = "הצעת מחיר"
            body = ""

            if request.method == 'POST' and request.FILES['file']:
                attachment = request.FILES['file']

            EmailService().send_email(receipts, subject, body, attachment.read())

            return Response({'s': "s"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'err': "Error"}, status=status.HTTP_400_BAD_REQUEST)


@ensure_csrf_cookie
def upload_image(request, folder):
    try:
        if request.method == 'POST' and request.FILES['file']:

            image = request.FILES['image']

            file_extension = os.path.splitext(image.name)[1]
            new_filename = get_random_string(10) + file_extension
            save_dir = os.path.join(settings.MEDIA_ROOT, folder)
            fs = FileSystemStorage(location=save_dir)
            filename = fs.save(new_filename, image)
            return Response({'image_url': [new_filename, filename]}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'err': f"Error {e}"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
