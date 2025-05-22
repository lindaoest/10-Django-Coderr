from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail, Order, Review
from auth_app.models import BusinessProfile
from django.contrib.auth.models import User
from rest_framework.exceptions import ParseError

""" Serializer for individual offer details """
class OfferDetailSerializer(serializers.ModelSerializer):
    # Show 'id' at OfferCreateUpdateSerializer in field details
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        extra_kwargs = {
            'title' : {'required': True},
            'revisions': {'required': True},
            'delivery_time_in_days': {'required': True},
            'price': {'required': True},
            'features': {'required': True},
            'offer_type': {'required': True},
        }

""" Serializer used for nested hyperlinked relationships """
class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}
        }

""" Serializer for reading offers, including related details and user info """
class OfferReadSerializer(serializers.ModelSerializer):
    # Display user as a primary key (read-only)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # Include related offer details as hyperlinks (read-only)
    details = OfferDetailHyperlinkedSerializer(many=True, read_only=True)
    # Add a computed field for user details
    user_details = serializers.SerializerMethodField()

    # Return business profile information of the offer's creator
    def get_user_details(self, obj):
        user = BusinessProfile.objects.get(user=obj.user)
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
            'updated_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
        }

""" Serializer used for creating and updating offers with nested offer details """
class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    # Include offer details as nested input
    details = OfferDetailSerializer(many=True)

    # Extract the minimum price from the first detail item
    def set_min_price(self, details):
        return details[0]['price']

    # Extract the minimum delivery time from the first detail item
    def set_min_delivery_time(self, details):
        return details[0]['delivery_time_in_days']

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    # Handle offer creation, including nested detail objects
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        min_price = self.set_min_price(details_data)
        min_delivery_time = self.set_min_delivery_time(details_data)
        offer = Offer.objects.create(min_price=min_price, min_delivery_time=min_delivery_time, **validated_data)

        # Create associated OfferDetail instances
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    # Handle offer update including updates to nested details
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        # Update offer fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        # Update existing OfferDetail instances
        if details_data:
            for detail_data in details_data:
                if 'offer_type' not in detail_data:
                    raise ParseError("Jeder Eintrag in 'details' muss ein 'offer_type'-Feld enthalten.")

                try:
                    detail = OfferDetail.objects.get(offer=instance.id, offer_type=detail_data['offer_type'])
                except OfferDetail.DoesNotExist:
                    raise ParseError(f"Kein OfferDetail mit offer_type '{detail_data['offer_type']}' gefunden.")

                detail.title = detail_data.get('title', detail.title)
                detail.revisions = detail_data.get('revisions', detail.revisions)
                detail.delivery_time_in_days = detail_data.get('delivery_time_in_days', detail.delivery_time_in_days)
                detail.price = detail_data.get('price', detail.price)
                detail.features = detail_data.get('features', detail.features)
                detail.save()

        return instance

""" Serializer for reading order data """
class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
            'updated_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
        }

""" Serializer for creating orders (uses offer_detail_id to generate order fields) """
class OrderCreateSerializer(serializers.ModelSerializer):
    # Accept offer_detail_id as input to base the order on a specific OfferDetail
    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'offer_detail_id', 'created_at', 'updated_at']
        # These fields are automatically filled in and should not be user-editable
        read_only_fields = ['customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
            'updated_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
        }

    # Create order based on selected offer detail and the current user
    def create(self, validated_data):
        pk = validated_data.pop('offer_detail_id')
        offerDetail = OfferDetail.objects.get(pk=pk.id)
        businessProfile = User.objects.get(pk=offerDetail.offer.user.id)
        customerProfile = User.objects.get(pk=self.context['request'].user.id)

        # Instantiate and return the new Order object
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

""" Serializer for updating orders """
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
            'updated_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
        }

""" Serializer for reading reviews (used in GET requests) """
class ReviewReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%S.%fZ"},
            'updated_at': {'format': "%Y-%m-%dT%H:%M:%S.%fZ"},
        }

""" Serializer for creating reviews """
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer']
        extra_kwargs = {
            'business_user': {'required': True},
            'rating': {'required': True},
            'description': {'required': True},
            'created_at': {'format': "%Y-%m-%dT%H:%M:%S.%fZ"},
            'updated_at': {'format': "%Y-%m-%dT%H:%M:%S.%fZ"},
        }

    # Create review and assign reviewer automatically from the request context
    def create(self, validated_data):
        user = User.objects.get(pk=validated_data['business_user'].id)
        review = Review.objects.create(business_user_id=user.id, **validated_data)
        return review

""" Serializer for updating reviews (business_user and reviewer are read-only) """
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user', 'reviewer']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%S.%fZ"},
            'updated_at': {'format': "%Y-%m-%dT%H:%M:%S.%fZ"},
        }