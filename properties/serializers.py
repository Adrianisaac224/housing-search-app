
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Property, PropertyImage, Amenity

# Amenity serializer
class AmenitySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Amenity
        geo_field = "location"
        fields = ['id', 'name', 'type', 'location']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

class PropertySerializer(GeoFeatureModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        geo_field = "location"
        fields = ('id', 'title', 'description', 'price', 'property_type', 'location', 'created_at', 'images', 'owner')
        read_only_fields = ('owner',)
