from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    post_link = serializers.CharField(max_length=195)
    post_title = serializers.CharField(max_length=195)
    post_author = serializers.CharField(max_length=195)
    post_details = serializers.CharField(max_length=195)