from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')

        response = Response({
            'status': True,
            'access_token': access_token
        })
        
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'],
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        
        return response
