from django.conf import settings
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializer import UserSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')
        # user = UserSerializer(request.user)

        response = Response({
            'status': True,
            # 'user': user.data,
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        
        # response.set_cookie(
        #     key=settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'],
        #     value=refresh_token,
        #     httponly=True,
        #     secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        #     samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        # )
        
        return response


class LogoutView (APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post (self, request):
#         try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(token=refresh_token)
            token.blacklist()

            return Response({
                'status': True
            })
#         except Exception as e:
#             return Response({
#                 'status': False,
#                 'error': 'Unauthorized user.'
#             }, status = status.HTTP_401_UNAUTHORIZED)