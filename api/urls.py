from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import LoginView, LogoutView, RegisterView, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register-user/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),

]
