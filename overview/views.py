from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from inventory.models import Storefront
from payments.models import StripeKeys
import stripe


@api_view(['POST'])
def get_overview_data(request):

    # GET STORE URL
    user_id_posted = request.data['user_id']
    store = Storefront.objects.get(user_id=user_id_posted)
    store_name = store.store_name

    return Response((store_name))