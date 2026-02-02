from pathlib import Path
from django.apps import apps as django_apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.routing.api.serializers import RoutePlanRequestSerializer
from apps.routing.services.router_client import OSRMClient
from apps.routing.services.geocoding_client import Geocoder
from apps.routing.domain.distance_utils import cumulative_miles
from apps.routing.domain.fuel_optimizer import plan_stops_by_state_segments

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class RoutePlanAPIView(APIView):
    def post(self, request):
        serializer = RoutePlanRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "start_lat" not in data:
            return Response(
                {"error": "Send coordinates for now: start_lat/start_lng/finish_lat/finish_lng"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_lat, start_lng = data["start_lat"], data["start_lng"]
        finish_lat, finish_lng = data["finish_lat"], data["finish_lng"]

        # 1) ruta (1 llamada)
        route = OSRMClient.get_route(start_lat, start_lng, finish_lat, finish_lng)
        coords = route["geometry"]["coordinates"]
        cum = cumulative_miles(coords)

        # 2) repo cargado en startup
        fuels_config = django_apps.get_app_config("fuels")
        repo = fuels_config.__class__.repo
        if repo is None:
            return Response({"error": "Fuel repo not loaded."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 3) geocoder con cache en data/
        base_dir = Path(__file__).resolve().parent.parent.parent.parent  # raíz del proyecto
        cache_path = base_dir / "data" / "geocode_cache.json"
        geocoder = Geocoder(cache_path=cache_path)

        try:
            plan = plan_stops_by_state_segments(
                cum_miles=cum,
                coords=coords,
                repo=repo,
                geocoder=geocoder,
                max_range_miles=500.0,
                mpg=10.0,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        return Response(
            {
                "route": route,
                "assumptions": {"max_range_miles": 500, "mpg": 10},
                "fuel_stops": [s.__dict__ for s in plan["stops"]],
                "total_fuel_cost": plan["total_cost"],
                "notes": "Using OSRM (routing) + Nominatim (reverse/geocode) with caching in data/geocode_cache.json",
            },
            status=status.HTTP_200_OK,
        )
