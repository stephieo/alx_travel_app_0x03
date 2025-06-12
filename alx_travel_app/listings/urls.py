from django.urls import path,include
from . import views
from rest_framework import routers 
from rest_framework_nested.routers import NestedDefaultRouter

router = routers.DefaultRouter()
router.register('listings', views.ListingViewSet)
router.register('bookings', views.BookingViewSet)

nested_messages_router = NestedDefaultRouter(router, r'listings', lookup='listings')
nested_messages_router.register(r'bookings', views.MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_messages_router.urls)),
    ]