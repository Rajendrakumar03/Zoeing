from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from v1.serializers.user_serializer import RegisterSerializer, LoginSerializer, UserSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


User = get_user_model()

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
    


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        if data['user_role'] == 'REGISTERED':
            
            email = data.get('email')
            try:
                user = User.objects.get(email=email)
                
                if user.user_role == 'GUEST':
                    user.user_role = 'REGISTERED'
                    user.set_password(data.get('password'))
                    user.save()
                    # tokens = get_tokens_for_user(user)
                    return Response(
                    {'message': 'Guest upgraded to registered user.','user': UserSerializer(user).data,'tokens': tokens,},status=status.HTTP_200_OK,)
                else:
                    return Response({'message': 'User already registered.'},status=status.HTTP_400_BAD_REQUEST,)
                
            except User.DoesNotExist:
                serializer = RegisterSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    # tokens = get_tokens_for_user(user)
                    return Response(
                        {
                            'message': 'Account created successfully.',
                            'user': UserSerializer(user).data,
                        },
                        status=status.HTTP_201_CREATED,
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif data['user_role'] == 'GUEST':
            
            if data['password'] and data['confirm_password']:
                data.pop("password")
                data.pop("confirm_password")
            
            users = User.objects.create(**data)
            
            if users:
            
                return Response("Guest user updated",status=status.HTTP_200_OK)
        
            return Response("Guest user not updated",status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

        if not user:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {'error': 'This account has been deactivated.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # tokens = get_tokens_for_user(user)
        return Response(
            {
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
        
        
class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class MeView(APIView):

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)

#         application_name = request.query_params.get("application", None)

#         user = User.objects.get(email=data["email"])

#         if user :
#             token_response = serializer.validated_data

#             response = Response(token_response, status=status.HTTP_200_OK)

#             return response


#         return Response({'error': "Invalid"},status=status.HTTP_401_UNAUTHORIZED)
