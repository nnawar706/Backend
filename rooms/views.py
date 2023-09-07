from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import *
from .serializer import *
from .models import ExamRoom

class ExamRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request):
        data = ExamRoom.objects.filter(user = request.user)

        serializer = ExamRoomSerializer(data, many=True)

        return JsonResponse({
            'status': True,
            'data': serializer.data
        }, status = 204 if len(serializer.data) == 0 else 200)

    def post(self, request):
        data = request.data

        serializer = ExamRoomSerializer(data = data)

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'errors': validation_error(serializer.errors)
            }, status = 422)

        room = serializer.create(serializer.validated_data)

        return JsonResponse({
            'status': True,
        }, status = 201)


def validation_error(errors):
    error_field = next(iter(errors))
    return errors[error_field][0]