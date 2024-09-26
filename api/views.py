from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.http import HttpResponse


@api_view(['GET'])
def home(request):
    html = """
    <html>
        <head>
            <title>Django_rest</title>
        </head>
        <body style="background-color: white; text-align: center; padding: 50px;">
            <h1 style="color: darkblue;">Welcome, Santhosh!</h1>
            <ul style="list-style-type: none; font-size: 18px; color: darkblue;">
                <li>Go and search the Below url's after the default API!</li>
                <li>add /api</li>
                <li>/users</li>
                <li>users/create</li>
            </ul>
        </body>
    </html>
    """
    return HttpResponse(html, content_type='text/html')

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)