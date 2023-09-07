from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import *
from .serializer import *
from .models import ExamRoom

class ExamRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get(self, request):
        data = ExamRoom.objects.filter(user = request.user)

        serializer = ExamRoomSerializer(data, many=True)

        return JsonResponse({
            'status': True,
            'data': serializer.data
        }, status = 204 if len(serializer.data) == 0 else 200)

    def post(self, request):
        data = request.data

        serializer = UserCreateSerializer(data = data)