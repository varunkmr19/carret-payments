from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from .models import Product, Transaction
from .serializers import ProductSerializer
import razorpay

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
    product_id = request.data.get('product_id')
    CURRENCY = 'INR'
    product = Product.objects.get(pk=product_id)
    user = request.user
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
      })
    else:
      return Response({
        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': 'Razorpay Error: Order creation failed',
      })
  except Product.DoesNotExist:
    return Response({
      'status': status.HTTP_500_BAD_REQUEST,
      'message': 'Invalid project_id: Product does not exist.',
    })
  except Exception as e:
    return Response({
      'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
      'message': str(e)
    })