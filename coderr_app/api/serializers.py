from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail, Order, Review, BaseInfo
from auth_app.models import BusinessProfile, CustomerProfile
class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        # read_only_fields = ['user']

class OfferSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'title', 'description', 'details', 'min_price', 'min_delivery_time', 'user']
        read_only_fields = ['user']

    def get_min_price(self, obj):
        return obj.details.first().price

    def get_min_delivery_time(self, obj):
        return obj.details.first().delivery_time_in_days

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderPostSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'offer_detail_id']
        read_only_fields = ['customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status']

    def create(self, validated_data):
        pk = validated_data.pop('offer_detail_id')
        offerDetail = OfferDetail.objects.get(pk=pk.id)
        businessProfile = BusinessProfile.objects.get(user_id=offerDetail.offer.user.id)
        customerProfile = CustomerProfile.objects.get(user_id=self.context['request'].user.id)

        order = Order.objects.create(
            business_user = businessProfile,
            customer_user = customerProfile,
            title = offerDetail.title,
            revisions = offerDetail.revisions,
            delivery_time_in_days = offerDetail.delivery_time_in_days,
            price = offerDetail.price,
            features = offerDetail.features,
            offer_type = offerDetail.offer_type,
            status = 'in_progress'
        )
        return order

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseInfo
        fields = '__all__'