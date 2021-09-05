from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from .models import Product, Transaction
from authentication.models import User
from .serializers import ProductSerializer
import razorpay
import json

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class ProductList(APIView):
  """
  List all products.
  """
  def get(self, request, format=None):
    try:
      products = Product.objects.all()
      serializer = ProductSerializer(products, many=True)
      return Response({
        'status': status.HTTP_200_OK,
        'message': 'List of products',
        'data': serializer.data
      })
    except:
      return Response({
        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': 'List of products failed',
      })

@api_view(['POST'])
def create_order(request):
  """
  Create an order.
  """
  try:
    print(request.data)
    product_id = request.data.get('product_id')
    auth_key = request.data.get('auth_key')
    CURRENCY = 'INR'
    product = Product.objects.get(pk=product_id)
    user = User.objects.get(auth_key=auth_key)
    order_amount = product.price

    # Call to razorpay api for new order creation
    order = client.order.create(
      dict(
        amount=order_amount,
        currency=CURRENCY,
        payment_capture='1'
      )
    )

    if order.get('id'):
      order_id = order.get('id')
      amount = order.get('amount')
      created_at = order.get('created_at')
      # store the order details in the database
      transaction = Transaction(user=user, product=product, order_id=order_id, total_amount=amount, created_at=created_at)
      transaction.save()
      return Response({
        'status': status.HTTP_200_OK,
        'message': 'Order created',
        'data': {
          'amount': amount,
          'order_id': order_id,
          'name': 'Carret Payments',
          'description': 'Test transaction'
        }
      })
    else:
      return Response({
        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': 'Razorpay Error: Order creation failed',
      })
  except Product.DoesNotExist:
    return Response({
      'status': status.HTTP_404_NOT_FOUND,
      'message': 'Invalid project_id: Product does not exist.',
    })
  except User.DoesNotExist:
    return Response({
    'status': status.HTTP_404_NOT_FOUND,
    'message': 'Invalid auth key'
    })
  except Exception as e:
    return Response({
      'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
      'message': str(e)
    })

@api_view(['POST'])
def verify_payment(request):
  res = json.loads(request.data.get('response'))
  
  razorpay_order_id = res.get('razorpay_order_id')
  razorpay_payment_id = res.get('razorpay_payment_id')
  razorpay_signature = res.get('razorpay_signature')

  order = Transaction.objects.get(order_id=razorpay_order_id)

  order.razorpay_order_id = razorpay_order_id
  order.razorpay_payment_id = razorpay_payment_id
  order.razorpay_signature = razorpay_signature

  data = {
    'razorpay_order_id': razorpay_order_id,
    'razorpay_payment_id': razorpay_payment_id,
    'razorpay_signature': razorpay_signature
  }

  check = client.utility.verify_payment_signature(data)

  if check is not None:
    # Payment failed
    order.payment_status = 'failed'
    order.save()
    return Response({
      'status': 500,
      'message': 'Something went wrong'
    })

  order.payment_status = "success"
  order.save()

  return Response({
    'status': status.HTTP_200_OK,
    'message': 'payment successfully received!'
  })