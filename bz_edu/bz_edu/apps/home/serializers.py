from rest_framework import serializers

from home.models import Banner, Nav


class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("img", 'link')
class NavModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = ("title", 'link','position')
