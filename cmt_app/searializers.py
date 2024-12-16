from rest_framework import serializers
from cmt_app.models import Guest , Movie , Reservation

class MovieSearializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields  = '__all__'

class ReservationSearializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields  = '__all__'

class GuestSearializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields  = ['pk' , 'reservation' , 'name' , 'mobile']





