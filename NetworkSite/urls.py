
from django.contrib import admin
from django.urls import path, include
from NetworkApp import views
from rest_framework import permissions
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register("signup", views.SignUpView, basename="signup")
router.register("login", views.LoginView, basename="login")
router.register("post",views.PostView, basename="post")
router.register("like",views.LikesView,basename="like")


schema_view = get_schema_view(
   openapi.Info(
      title="NetworkSite API",
      default_version='v1',
      description="NetworkSite APIs",
      contact=openapi.Contact(email=" "),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api-auth/', include('rest_framework.urls')),
   path('', include(router.urls)),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
