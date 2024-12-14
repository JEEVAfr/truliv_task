from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.common.views.base import *

# schedule a visit create api view only is to visit the room
class ScheduleVisitCreateAPIView(AppAPIView):
    
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):

        serializer = ScheduleVisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })