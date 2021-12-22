from django.shortcuts import render
import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

#stripe.api_key = settings.STRIPE_SECRET


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='EUR',
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=200, data=test_payment_intent)


@api_view(['POST'])
def create_customer(request):
    data = request.data
    print(data)
    email = data['email']
    payment_method_id = data['payment_method_id']
    show_message = False
    extra_msg = ""

    # Check if the customer email already exists in Stripe as a customer
    customer_data = stripe.Customer.list(email=email).data

    # If the customer doesn't exist
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id)

    else:
        customer = customer_data[0]
        extra_msg = "Customer already exists!"
        show_message = True

    return Response(status=200,
                    data={
                        'message': 'Success',
                        'data': {'customer_id': customer.id},
                        'extra_msg': extra_msg,
                        'show_message': show_message
                    })
