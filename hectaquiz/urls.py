from django.contrib import admin
from django.urls import re_path, path, include

from rest_framework_simplejwt import views as jwt_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
    openapi.Info(
        title="Hectaquiz App",
        default_version="v1",
        description="Welcome to Hectaquiz",
        terms_of_service="http://example.com/terms/",
        contact=openapi.Contact(email="adenikeawofeso@gmail.com"),
        license=openapi.License(name="Awesome IP")
    ),
    public=True,
    permission_classes =(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'), 
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'), 
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('quiz.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls'))
]
