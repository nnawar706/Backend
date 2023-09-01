from rest_framework.views import APIView
from rest_framework import permissions
from django.http import JsonResponse
from .serializer import UserCreateSerializer, UserSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        data = request.data

        serializer = UserCreateSerializer(data = data)
        
        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'errors': validation_error(serializer.errors)
            }, status = 422)

        user = serializer.create(serializer.validated_data)
        # user = UserSerializer(user)
        return JsonResponse({
            'status': True,
            # 'data': user.data
        }, status = 201)


class RetrieveUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pass


def validation_error(errors):
    error_field = next(iter(errors))
    return errors[error_field][0]