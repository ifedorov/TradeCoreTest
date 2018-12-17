from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path

from tradetestapp.views import PostViewSet, UserCreateViewSet

urlpatterns = [
    path(r'user/login/', obtain_jwt_token),
    path(r'user/signup/', UserCreateViewSet.as_view({'post': 'create'})),
]
router = routers.SimpleRouter()
router.register(r'post', PostViewSet)
urlpatterns += router.urls
