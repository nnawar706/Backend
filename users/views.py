from rest_framework.views import APIView
from rest_framework import permissions, status
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request):
        data = request.data

        User.objects.create_user(
            data['name'],
            data['email'],
            data['password']
        )

        return JsonResponse({
            'status': True
        }, status = status.HTTP_201_CREATED)


class RetrieveUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pass