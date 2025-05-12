from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail, Order, Review
from auth_app.models import BusinessProfile
from django.contrib.auth.models import User

class OfferDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}
        }

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailSerializer(many=True, write_only=True)
    details_read = OfferDetailHyperlinkedSerializer(many=True, source='details', read_only=True)
    user_details = serializers.SerializerMethodField()

    def get_user_details(self, obj):
        user = BusinessProfile.objects.get(user=obj.user)
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['details'] = rep.pop('details_read', None)
        return rep

    class Meta:
        model = Offer
        fields = ['id', 'title', 'description', 'image', 'details', 'details_read', 'min_price', 'min_delivery_time', 'user', 'user_details', 'created_at', 'updated_at']
        read_only_fields = ['user', 'details_read', 'user_details', 'min_price', 'min_delivery_time']

    def get_min_price(self, details):
        return details[0]['price']

    def get_min_delivery_time(self, details):
        return details[0]['delivery_time_in_days']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        min_price = self.get_min_price(details_data)
        min_delivery_time = self.get_min_delivery_time(details_data)
        offer = Offer.objects.create(min_price=min_price, min_delivery_time=min_delivery_time, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        for detail_data in details_data:
            detail = OfferDetail.objects.get(pk=detail_data['id'])
            detail.title = detail_data.get('title', detail.title)
            detail.revisions = detail_data.get('revisions', detail.revisions)
            detail.delivery_time_in_days = detail_data.get('delivery_time_in_days', detail.delivery_time_in_days)
            detail.price = detail_data.get('price', detail.price)
            detail.features = detail_data.get('features', detail.features)
            detail.save()

        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderPostSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'offer_detail_id', 'created_at', 'updated_at']
        read_only_fields = ['customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status']

    def create(self, validated_data):
        pk = validated_data.pop('offer_detail_id')
        offerDetail = OfferDetail.objects.get(pk=pk.id)
        businessProfile = User.objects.get(pk=offerDetail.offer.user.id)
        customerProfile = User.objects.get(pk=self.context['request'].user.id)

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

class OrderPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']

class ReviewReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer']

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data['business_user'].id)
        review = Review.objects.create(business_user_id=user.id, **validated_data)
        return review

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user', 'reviewer']