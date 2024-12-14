from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import *
from rest_framework.pagination import PageNumberPagination
from apps.common.views.base import *


# pagination
class AppPagination(PageNumberPagination):
    page_size = 10

class BlogListCreateAPIView(AppAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        blog = Blog.objects.all()
        paginator = AppPagination()
        paginated_blog = paginator.paginate_queryset(blog, request)
        serializer = BlogSerializers(paginated_blog, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = BlogSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

class BlogDetailAPIView(AppAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        serializer = BlogSerializers(blog)
        return self.send_response({
            "data": serializer.data
        })

    def patch(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        serializer = BlogSerializers(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        blog.delete()
        return self.send_response({
            "message": "BLOG deleted successfully."
        })

