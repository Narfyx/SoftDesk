from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtainPairView, UserCreate, UserDetail

urlpatterns = [
    path("register/", UserCreate.as_view(), name="register"),
    path(
        "<int:user_pk>/token/",
        MyTokenObtainPairView.as_view(),
        name="my_token_obtain_pair",
    ),
    path(
        "<int:user_pk>/token-refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("<int:user_pk>/", UserDetail.as_view(), name="user_detail"),
]
