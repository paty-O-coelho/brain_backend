from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from producers.views import ProducerViewSet, FarmViewSet, HarvestViewSet, CropViewSet

# Importações do drf-yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r"producers", ProducerViewSet)
router.register(r"farms", FarmViewSet)
router.register(r"harvests", HarvestViewSet)
router.register(r"crops", CropViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Brain API",
        default_version="v1",
        description="API documentation for Brain project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Rotas do Swagger:
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
