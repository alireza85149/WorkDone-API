from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/accounts/', include('apps.accounts.api.urls'),),
    path("api/projects/",include("apps.projects.api.urls"),),
    path("api/proposals/",include("apps.proposals.api.urls"),),
    path("api/contracts/",include("apps.contracts.api.urls"),),
    path("api/reviews/", include("apps.reviews.api.urls"),),
]
