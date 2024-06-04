from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtainPairView, UserCreate, UserDetail

urlpatterns = [
    path("register/", UserCreate.as_view(), name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "me/", UserDetail.as_view(), name="user_detail"
    ),  # Route pour récupérer, mettre à jour et supprimer le compte de l'utilisateur
]
