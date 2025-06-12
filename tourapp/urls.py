from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet, basename='destination')

urlpatterns = [
    # API endpoints
    *router.urls,

    # Web views
    path('', views.index, name='index'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('create/', views.create_destination, name='create_destination'),
    path('destination/<int:pk>/edit/', views.update_destination, name='update_destination'),
    path('destination/<int:pk>/delete/', views.delete_destination, name='delete_destination'),

]
