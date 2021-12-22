from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from allauth.account.models import EmailAddress
from django.conf import settings


@api_view(['POST'])
def check_email_exists(request):
    """ 
    This view takes in an email address and returns True is the email exists in the db
    It returns False if the email does not exist in the db
    """
    if request.method == 'POST':
        email = request.data['email']
        if EmailAddress.objects.filter(email=email).exists():
            return Response(True)
        else:
            return Response(False)


@api_view(['POST'])
def check_email_verified(request):
    """
    This view takes in an email address and truens True if the email is verified
    It will return False if the email is not verified OR if the email does not exist in the db
    """
    if request.method == 'POST':
        email = request.data['email']
        if EmailAddress.objects.filter(email=email).exists():
            user = EmailAddress.objects.get(email=email)
            if user.verified:
                return Response(True)
            else:
                return Response(False)
        else:
            return Response(False)



