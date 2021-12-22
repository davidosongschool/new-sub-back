from django.shortcuts import render
from .models import Inventory, Storefront
from .serializers import InventorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from payments.models import StripeKeys
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse



#stripe
import stripe


# Get list of all products from Stripe Products - Pass active parameter to exclude archieved products 
# This is not a protected view and will get a list of products once a user id is passed in the post data 
@api_view(['POST'])
def product_list(request):

    if request.method == 'POST':

        user_id_posted = request.data['user_id']
        key = StripeKeys.objects.get(pk=user_id_posted)
        stripe.api_key = key.secret_key

        products = stripe.Product.list(active=True)
        return Response(products)


# Get list of all products from Stripe Products - Pass active parameter to exclude archieved products 
@api_view(['POST'])
def storefront_product_list(request):

        store_name = request.data['store_name']
        
        #Get User associated with store name
        try:
            store = Storefront.objects.get(store_name=store_name)
        except Storefront.DoesNotExist:
            return Response("Store Does Not Exist")

        print (store.user_id.pk)
        key = StripeKeys.objects.get(pk=store.user_id.pk)
        stripe.api_key = key.secret_key

        products = stripe.Product.list(active=True)
        return Response(products)


#Get Individual Product - Take in Store Name and Product ID 

@api_view(['POST'])
def storefront_single_product(request):

    store_name = request.data['store_name']
    product_id = request.data['product_id']
    print(product_id)

    
    #Get User associated with store name
    try:
        store = Storefront.objects.get(store_name=store_name)
    except Storefront.DoesNotExist:
        return Response("Store Does Not Exist")
    
    #Get the product details based on the pruct ID and User 
    try:
        product = Inventory.objects.get(product_stripe_id=product_id, user_id=store.user_id.pk)
    except:
        return Response("Product not found")

    data = InventorySerializer(product).data

    return Response(data)

# Create A Product

# For security - To prevent anyone from posting a user id and creating a product, the client must provide a token that will be matched with a user_id 
# Therefore, they must be logged in as that user in order to make requests to Stripe associated with that secret key
@api_view(['POST'])
def create_product(request):

    if request.method == 'POST':
        name = request.data['name']
        description = request.data['description']

        token_posted = request.data['token']

        """ 
        Look for user based on token passed - If the token doesn't match a user, then throw an 404 error - This should ensure that in order to make changes
        using a stripe key stored in the db, you have to have the user access token 
        """
        try:
            user = Token.objects.get(key=token_posted)
        except Token.DoesNotExist:
            raise Http404("Cant find a user associated with those details!")

        userId = user.user.id
        associated_user = User.objects.get(pk=userId)
        key = StripeKeys.objects.get(pk=userId)
        stripe.api_key = key.secret_key
        createdProduct = stripe.Product.create(name=name, description=description)

        # When a product is created in stripe, it is then stored in the Inventory model with the associated 
        new_product = Inventory.objects.create(product_name=name, product_stripe_id=createdProduct.id, user_id= associated_user, product_description=description)

        return Response(createdProduct.id)



# Create A Price 
@api_view(['POST'])
def set_price(request):
    if request.method == 'POST':

        token_posted = request.data['token']
        try:
            user = Token.objects.get(key=token_posted)
        except Token.DoesNotExist:
            raise Http404("Cant find a user associated with those details!")

        userId = user.user.id
        key = StripeKeys.objects.get(pk=userId)
        #stripe.api_key = key.secret_key
    

        # Multiply price by 100 to get it in EUR 
        cost = int(request.data['price']) * 100 
        id = request.data['id']
        price = stripe.Price.create(
        product=id,
        unit_amount=cost,
        currency='EUR',  
        recurring={
        'interval': 'month',
        })

        # Set Price in Django DB for displaying 
        product = Inventory.objects.get(product_stripe_id=id)
        product.price = int(request.data['price'])
        product.save()


        return Response(price)





# Check that a store exists 
@api_view(['POST'])
def store_front(request):

    if request.method == 'POST':
        posted_store_name = request.data['store']
        try:
            check_store_exists = Storefront.objects.get(store_name=posted_store_name)
            return Response(True)
        except Storefront.DoesNotExist:
            return Response(False)

