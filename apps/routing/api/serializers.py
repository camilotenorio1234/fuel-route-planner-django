from rest_framework import serializers


class RoutePlanRequestSerializer(serializers.Serializer):
    # modo recomendado: coords (cero llamadas extra)
    start_lat = serializers.FloatField(required=True)
    start_lng = serializers.FloatField(required=True)
    finish_lat = serializers.FloatField(required=True)
    finish_lng = serializers.FloatField(required=True)
