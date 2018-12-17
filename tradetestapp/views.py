from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from tradetestapp.models import Post
from tradetestapp.serializers import (
    PostSerializer,
    UserSerializer,
    LikeSerializer,
    UnlikeSerializer,
)


class PostViewSet(CreateAPIView, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def like(self, request, pk):

        post = self.get_object()

        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def unlike(self, request, pk):
        post = self.get_object()

        serializer = UnlikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserCreateViewSet(CreateAPIView, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
