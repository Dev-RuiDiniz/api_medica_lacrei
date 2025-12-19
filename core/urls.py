from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Importações para a documentação
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),

    # Endpoints de Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- Documentação da API ---
    # Gera o arquivo de esquema (YAML/JSON) que descreve a API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Interface Interativa Swagger UI (ideal para testes rápidos)
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Interface Redoc (documentação mais limpa e focada em leitura técnica)
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
