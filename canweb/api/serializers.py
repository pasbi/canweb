from rest_framework import serializers
from api.models import Song

class SongDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('label', 'pattern', 'pk')

class SongLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('label', 'pk', 'pattern')