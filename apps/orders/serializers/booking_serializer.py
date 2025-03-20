from datetime import datetime, timedelta

from rest_framework import serializers

from apps.orders.models import Booking
from apps.orders.serializers import OrderSerializer
from apps.engineers.serializers import EngineerReadSerializer
from apps.common.booking_utils import compute_interval
from apps.common.enums import BookingStatusType


class BookingSerializer(serializers.ModelSerializer):
    booking_start = serializers.SerializerMethodField(read_only=True)
    booking_end = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'order', 'engineer',
            'booking_date', 'booking_time',
            'duration', 'booking_status',
            'remarks', 'booking_start', 'booking_end',
        ] #==> duration example: 1 12:20:00 (for 1 days 12 hr 20 mins)
        read_only_fields = ['id', 'booking_end']

    def get_booking_end(self, obj):
        date_str = obj.booking_date.strftime('%Y-%m-%d')
        time_str = obj.booking_time.strftime('%H:%M:%S')

        duration_str = str(obj.duration)
        _, booking_end = compute_interval(date_str, time_str, duration_str)
        return booking_end

    def get_booking_start(self, obj):
        date_str = obj.booking_date.strftime('%Y-%m-%d')
        time_str = obj.booking_time.strftime('%H:%M:%S')

        duration_str = str(obj.duration)
        booking_start, _ = compute_interval(date_str, time_str, duration_str)
        return booking_start

    def validate(self, data):
        engineer = data.get('engineer')
        booking_date = data.get('booking_date')
        booking_time = data.get('booking_time')
        duration_str = str(data.get('duration'))  # Example: "1 12:20:00"

        date_str = booking_date.strftime('%Y-%m-%d') # 2025-04-23
        time_str = booking_time.strftime('%H:%M:%S') # 12:23:02
        new_booking_start, new_booking_end = compute_interval(date_str, time_str, duration_str)

        existing_bookings = Booking.active_objects.filter(engineer=engineer)

        for existing_booking in existing_bookings:
            existing_start, existing_end = compute_interval(
                existing_booking.booking_date.strftime('%Y-%m-%d'),
                existing_booking.booking_time.strftime('%H:%M:%S'),
                str(existing_booking.duration)
            )
            print()
            print()
            print(f"Existing: {existing_start} - {existing_end}")
            print(f"New: {new_booking_start} - {new_booking_end}")
            print()
            print()

            if new_booking_start < existing_end and new_booking_end > existing_start:
                raise serializers.ValidationError("Booking interval overlaps with an existing booking.")

        return data


class BookingDetailsSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    engineer = EngineerReadSerializer(read_only=True)
    # booking_end = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'order', 'engineer',
            'booking_date', 'booking_time',
            'duration', 'booking_status',
            'remarks',
        ]
