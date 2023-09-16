from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .serializer import *
from .permissions import *


class QuestionCreateView (APIView):
    permissions = [permissions.IsAuthenticated, IsTeacher]

    def post (self, request):
        data = request.data

        serializer = QuestionCreateSerializer (data = data, context = {'request': request})

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': serializer.errors
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        return JsonResponse({'status': True}, status = status.HTTP_201_CREATED)