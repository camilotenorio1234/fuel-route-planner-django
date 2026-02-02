from django.urls import path
from .views import RoutePlanAPIView

urlpatterns = [
    path("route-plan/", RoutePlanAPIView.as_view(), name="route-plan"),
]
