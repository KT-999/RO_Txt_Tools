from django.utils.timezone import now
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # days = serializers.SerializerMethodField()

    class Meta:
        model = User
        # days_since_created = 'test'
        fields = '__all__'
        # fields = ['url', 'username', 'email', 'is_staff', 'days']

    # def get_days(self, obj):
    #     return (now() - obj.date_joined).days
