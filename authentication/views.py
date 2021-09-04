import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . models import User

# Create your views here.
def get_csrf(request):
  csrf_token = get_token(request)
  response = {
    'status': 200,
    'message': 'CSRF cookie set',
    'data': {
      'csrf': csrf_token
    }
  }
  return JsonResponse(response, status=200)

@require_POST
def login_view(request):
  data = json.loads(request.body)
  username = data.get('username')
  password = data.get('password')

  if username is None or password is None:
    return JsonResponse({'message': 'Please provide username and password.'}, status=400)

  user = authenticate(username=username, password=password)

  if user is None:
      return JsonResponse({'message': 'Invalid credentials.'}, status=400)

  login(request, user)
  return JsonResponse({
    'message': 'Successfully logged in.',
    'data': {
      'auth_key': user.auth_key
    }
    }, status=200)

def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'message': 'Successfully logged out.'}, status=200)

@require_POST
def register_view(request):
  data = json.loads(request.body)
  username = data.get('username')
  email = data.get('email')

  # Ensure password matches confirm password
  password = data.get('password')
  confirm_passowrd = data.get('confirm_password')
  if password != confirm_passowrd:
    return JsonResponse({'message': 'Passwords do not match.'}, status=400)

  # Attempt to create new user
  try:
    user = User.objects.create_user(username, email, password)
    user.save()
  except IntegrityError:
    return JsonResponse({'message': 'Username already taken.'}, status=400)
  
  login(request, user)
  return JsonResponse({'message': 'Successfully registered.'}, status=200)


def get_auth_key(request):
  if request.user.is_authenticated:
    auth_key = request.user.auth_key
    return JsonResponse({
      'message': 'Success',
      'data': {
        'auth_key': auth_key
      }
    }, status=200)

  return JsonResponse({'message': 'Not logged in'}, status=400)

class SessionView(APIView):
  authentication_classes = [SessionAuthentication, BasicAuthentication]
  permission_classes = [IsAuthenticated]

  @staticmethod
  def get(request, format=None):
    return JsonResponse({'isAuthenticated': True})

