from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsOwner
from .serializers import UserSerializer, ShowAllUsersSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ShowAllUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ShowAllUsersSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [IsOwner]


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]  # Default for all methods

    def get_permissions(self):
        # Set specific permissions for each method
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsOwner]
        elif self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get(self, request):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = self.get_object()
        serializer = UserSerializer(
            user, data=request.data, partial=True
        )  # Utilisation de `partial=True` pour les mises à jour partielles
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user
