from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .permissions import *
from .serializer import *
from .models import ExamRoom

class ExamRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request):
        if request.query_params:
            data = ExamRoom.objects.filter(user = request.user, **request.query_params.dict()).order_by('-created_at')
        else:
            data = ExamRoom.objects.filter(user = request.user).order_by('-created_at')

        serializer = ExamRoomSerializer(data, many=True)

        return JsonResponse({
            'status': True,
            'data': serializer.data
        }, status = status.HTTP_204_NO_CONTENT if len(serializer.data) == 0 else status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        serializer = ExamRoomCreateSerializer(data = data, context={'request': request})

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': validation_error(serializer.errors)
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        room = serializer.create(serializer.validated_data)

        return JsonResponse({
            'status': True,
        }, status = status.HTTP_201_CREATED)


class RetrieveExamRoomView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request, pk):
        try:
            data = ExamRoom.objects.get(pk=pk)

            if data.user != request.user:
                return JsonResponse({
                    'status': False,
                    'error': 'You are not allowed to access the data.'
                }, status = status.HTTP_403_FORBIDDEN)
        except ExamRoom.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Room does not exist.'
            }, status = status.HTTP_404_NOT_FOUND)

        serializer = ExamRoomSerializer(data, many=False)

        return JsonResponse({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            room = ExamRoom.objects.get(pk=pk)
        except ExamRoom.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Room does not exist.'
            }, status = status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = ExamRoomUpdateSerializer(instance = room, data = data)

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': validation_error(serializer.errors)
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        room = serializer.update(instance = room, data = serializer.validated_data)

        return JsonResponse({
            'status': True,
        }, status = status.HTTP_200_OK)


def validation_error(errors):
    error_field = next(iter(errors))
    return errors[error_field][0]