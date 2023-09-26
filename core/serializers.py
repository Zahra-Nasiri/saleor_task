from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # Use write_only to hide password in responses
