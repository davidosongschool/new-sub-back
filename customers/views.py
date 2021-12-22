from rest_framework.response import Response
from rest_framework.decorators import api_view
from payments.models import StripeKeys
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse

#stripe
import stripe

# Get list of all products from Stripe Products - Pass active parameter to exclude archieved products 
# This is not a protected view and will get a list of products once a user id is passed in the post data 
@api_view(['POST'])
def cutomer_list(request):

    if request.method == 'POST':

        user_id_posted = request.data['user_id']
        key = StripeKeys.objects.get(pk=user_id_posted)
        stripe.api_key = key.secret_key

        customers = stripe.Product.list(active=True)
        return Response(customers)