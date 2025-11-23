from rest_framework import serializers
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()  # dynamic field

    class Meta:
        model = Dataset
        fields = ['id', 'original_filename', 'row_count', 'uploaded_at', 'summary']

    def get_summary(self, obj):
        return obj.get_summary() or {} # call model method
