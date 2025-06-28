
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from .models import Property, Amenity
from .serializers import PropertySerializer, AmenitySerializer
# Amenity ViewSet
class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    def get_queryset(self):
        qs = self.queryset
        type_filter = self.request.query_params.get('type')
        if type_filter:
            qs = qs.filter(type=type_filter)
        return qs


class PropertyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

    def get_queryset(self):
        queryset = Property.objects.all()
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius')  # in meters
        polygon = self.request.query_params.get('polygon')

        if lat and lon and radius:
            user_location = Point(float(lon), float(lat), srid=4326)
            queryset = queryset.annotate(distance=Distance('location', user_location))\
                               .filter(location__distance_lte=(user_location, float(radius)))\
                               .order_by('distance')

        elif polygon:
            try:
                geom = GEOSGeometry(polygon, srid=4326)
                queryset = queryset.filter(location__within=geom)
            except Exception as e:
                print(f"Invalid polygon: {e}")

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Create your views here.
