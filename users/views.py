from rest_frameworks import APIView, permissions, status
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(APIView):
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