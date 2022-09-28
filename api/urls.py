from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.urls import path, include
from . import views

app_name = 'api'

receita_api_urls = SimpleRouter()
receita_api_urls.register(
    prefix='receitas',
    viewset=views.ReceitaModelViewSet,
    basename='receitas-api'
)

usuario_api_urls = SimpleRouter()
usuario_api_urls.register(
    'usuarios',
    views.UserReadOnlyModelViewSet,
    'usuarios-api'
)


urlpatterns = [
    path('', include(receita_api_urls.urls)),
    path('', include(usuario_api_urls.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
