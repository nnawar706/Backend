from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import permissions
from .serializer import *
from .models import ExamRoom

class ExamRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        data = ExamRoom.objects.all()

        serializer = ExamRoomSerializer(data, many=True)

        return JsonResponse({
            'status': True,
            'data': serializer.data
        }, status = 204 if len(serializer.data) == 0 else 200)