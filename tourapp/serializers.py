from rest_framework import serializers
from .models import Destination, DestinationImage


class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = ['id', 'image']

class DestinationSerializer(serializers.ModelSerializer):
    images = DestinationImageSerializer(many=True, read_only=True)
    add_image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Destination
        fields = [
            'id',
            'place_name',
            'weather',
            'state',
            'district',
            'map_link',
            'description',
            'images',
            'add_image',  # 👈 this adds the file upload option in API UI
        ]

    def create(self, validated_data):
        image = validated_data.pop('add_image', None)
        destination = Destination.objects.create(**validated_data)
        if image:
            DestinationImage.objects.create(destination=destination, image=image)
        return destination

    def update(self, instance, validated_data):
        image = validated_data.pop('add_image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if image:
            DestinationImage.objects.create(destination=instance, image=image)
        return instance

