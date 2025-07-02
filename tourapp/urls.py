from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import DestinationViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet, basename='destination')

urlpatterns = [
    # API routes
    *router.urls,

    # Web views
    path('', views.index, name='index'),
    path('about/', views.about_view, name='about'),
    path('create/', views.create_destination, name='create_destination'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('destination/<int:pk>/edit/', views.update_destination, name='update_destination'),
    path('destination/<int:pk>/delete/', views.delete_destination, name='delete_destination'),

    # ✅ Fixed route (was causing error)
    path('destination/', views.destination_view, name='destination'),

    # Optional: static carousel-style page
    path('static-destinations/', views.static_destinations_list, name='static_destinations'),
]
