from rest_framework import serializers
from .models import DetectionResult, DetectedObject

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class DetectedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedObject
        fields = ['class_name', 'confidence', 'bbox_x1', 'bbox_y1', 'bbox_x2', 'bbox_y2']

class DetectionResultSerializer(serializers.ModelSerializer):
    detected_objects = DetectedObjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = DetectionResult
        fields = ['id', 'original_image', 'annotated_image', 'uploaded_at', 'detected_objects']