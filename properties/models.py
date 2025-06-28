

from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=50)  # e.g., apartment, house
    location = models.PointField(geography=True)     # Geo field (lat/lon)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.owner.username}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')


    def __str__(self):
        return f"{self.property.title} Image"


# Amenity model
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)  # e.g. school, hospital, shop
    location = models.PointField(geography=True)

    def __str__(self):
        return f"{self.type}: {self.name}"
