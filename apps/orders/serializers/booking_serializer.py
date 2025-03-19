from rest_framework import serializers

from apps.orders.models import Booking
from apps.orders.serializers import OrderSerializer
from apps.engineers.serializers import EngineerReadSerializer


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'order', 'engineer',
            'booking_date', 'booking_time',
            'duration', 'booking_status',
            'remarks',
        ]


class BookingDetailsSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    engineer = EngineerReadSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'order', 'engineer',
            'booking_date', 'booking_time',
            'duration', 'booking_status',
            'remarks',
        ]
