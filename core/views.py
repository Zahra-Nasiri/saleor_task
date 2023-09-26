from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
import requests


class LogInUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            query = """
            mutation($email: String!, $password: String!) {
            tokenCreate(email: $email, password: $password) {
                token
                refreshToken
                errors {
                field
                message
                    }
                }
            }
            """
            variables = {
                "email": email,
                "password": password
            }
            url = 'http://localhost:8000/graphql/'
            headers = {}
            response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
            data = response.json()['data']['tokenCreate']
            refresh_token = data['refreshToken']
            token = data['token']
            if token and refresh_token:
                return Response({'refresh_token': refresh_token, 'token': token})
            return Response({'message': data['errors']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

