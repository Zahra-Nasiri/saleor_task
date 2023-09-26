from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer, CategorySerializer
import requests
import json


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


class CategoryView(APIView):    
    def get(self, request):
        after = request.GET.get('after', '')
        first = request.GET.get('first', 10)
        url = "http://localhost:8000/graphql/"
        query = """
        query ($first: Int!, $after: String) {
        categories(first: $first, after: $after) {
            pageInfo {
            hasNextPage
            hasPreviousPage
            startCursor
            endCursor
            }
            edges {
            node {
                id
                name
                slug
            }
            }
        }
        }
        """
        variables = {
            "first": first,
            "after": after 
        }
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()['data']['categories']        

        return Response(data)


    def post(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = authorization_header.split('Bearer ')[-1] if 'Bearer ' in authorization_header else ''
        url = 'http://localhost:8000/graphql/'
        query = """
        mutation($name: String!, $slug: String!) {
        categoryCreate(input: { name: $name, slug: $slug }) {
            errors {
            field
            message
            }
            category {
            id
            name
                }
            }
        }
        """

        if token:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                name = serializer.validated_data['name']
                slug = serializer.validated_data['slug']
                variables = {
                    "name": name,
                    "slug": slug
                }
                response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
                errors = response.json().get('errors', None)
                data = response.json()["data"]["categoryCreate"]
                if not errors:
                    errors = data.get('errors', None)
                    category = data.get('category', None)
                    if not errors:
                        return Response(category, status=status.HTTP_200_OK)
                    return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": errors[0]['message']}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

        return Response({'message': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class ProductsView(APIView):
    def post(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = authorization_header.split('Bearer ')[-1] if 'Bearer ' in authorization_header else ''
        data = request.data
        name = data.get('name', None)
        product_type = data.get('product_type', None)
        category_type = data.get('category_type', None)
        headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
        }
        query = """
        mutation createProduct($input: ProductCreateInput!) {
            productCreate(input: $input) {
                errors {
                field
                code
                message
                }
                product {
                name
                id
                productType {
                    id
                }
                category {
                    id
                }
                }
            }
            }
        """
        variables = {
            "input": {
                "name": name,
                "productType": product_type,
                "category": category_type
            }

        }
        url = 'http://localhost:8000/graphql/'
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        return Response(response.json())
