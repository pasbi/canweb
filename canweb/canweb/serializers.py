from rest_framework import serializers
from api.models import Song

# class SongSerializer(serializers.Serializer):
#     def create(self, validated_data):
#         return Can.object.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.label = validated_data.get('label', instance.label)
#         instance.pattern = validated_data.get('pattern', instance.pattern)
#         instance.save()
#         return instance

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('label', 'pattern')