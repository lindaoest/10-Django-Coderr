from rest_framework import serializers
from coderr_app.models import Offer, OfferOption, Order, Review

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class OfferOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferOption
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'