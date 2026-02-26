from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentSearchSerializer(serializers.ModelSerializer):
    score = serializers.FloatField()
    url = serializers.HyperlinkedIdentityField(
        view_name='document-detail',
        lookup_field='pk'
    )