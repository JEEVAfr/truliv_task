from .models import *
from rest_framework import serializers

# blog serializers
class BlogSerializers(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['blog_title', 'blog_description']