from rest_framework import serializers
from .models import Order, Product, OrderItem
"""
Converting model instances to JSON (so you can send them in an API response).
Validating and converting incoming JSON to model instances (so you can save data from API requests).
"""


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product  # → this serializer is for the Product model.
        fields = (
            'id', 'name', 'description', 'price', 'stock'
        )  # → these are the model fields you want to include in the API.

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Price must be a positive value.")
        return value

    #DRF automatically calls validate_<fieldname> for the field when data is being deserialized or saved via the API.
