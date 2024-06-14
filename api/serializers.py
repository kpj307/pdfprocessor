from rest_framework import serializers
from .models import PdfData

class PdfDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfData
        fields = '__all__'
