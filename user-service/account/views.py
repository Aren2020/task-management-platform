from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer

class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            user = serializer.save()
            refresh = RefreshToken.for_user(user) # Создание Refesh и Access
            refresh.payload.update({    # usefull information
                'user_id': user.id,
                'username': user.username,
                'email': user.email, # Add necessary fields
            })

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Login and password is required'},
                            status = status.HTTP_400_BAD_REQUEST)

        user = authenticate(username = username, password = password)
        if user is None:
            return Response({'error': 'Invalid data'},
                            status = status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status = status.HTTP_200_OK)
    
class LogoutAPIView(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token') # Client should send refresh token
        if not refresh_token:
            return Response({'error': 'Refresh token required'},
                            status = status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist() # Add token to blacklist
        except Exception as e:
            return Response({'error': 'Invalid Refresh token'},
                            status = status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Logout successfully'}, status = status.HTTP_200_OK)

class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })