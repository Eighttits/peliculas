from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from trailers import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'actors', views.ActorViewSet)
router.register(r'directors', views.DirectorViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'trailers', views.TrailerViewSet)
router.register(r'savedmovies', views.SavedMovieViewSet, basename='savedmovies')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('create-user/', views.UserCreateView.as_view(), name='create-user'),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify-token/', views.VerifyTokenView.as_view(), name='verify_token'),
]
