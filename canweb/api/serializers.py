from rest_framework import serializers
from api.models import Song

class SongDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('label', 'pattern')

class SongLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('label',)