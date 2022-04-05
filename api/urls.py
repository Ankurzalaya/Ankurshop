from django.urls import include, path
from rest_framework import routers

# swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from .views import (
    ProductViewSet,
    CategoryViewSet,
    OrderViewSet,
    AdressViewSet,
    WishlistViewSet,
    SearchListView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Ankurshop",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r"Products", ProductViewSet)
router.register(r"Category", CategoryViewSet)
router.register(r"Adress", AdressViewSet)
router.register(r"Order", OrderViewSet)
router.register(r"Wishlist", WishlistViewSet)
# router.register(r"search",ProductListView)


urlpatterns = [
    path("", include(router.urls)),
    path("search/", SearchListView.as_view(), name="search"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    #  path("gettoken/", obtain_auth_token),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # path('^swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # path("wishlist",listWishlist.as_view(),name="wishlist"),
]
