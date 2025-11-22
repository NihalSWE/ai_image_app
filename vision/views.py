from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageUploadSerializer
from .utils import detect_objects
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import DetectionResult, DetectedObject

def validate_image_file(file):
    """Validate uploaded image file"""
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
    max_size = 10 * 1024 * 1024  # 10MB
    
    if file.content_type not in allowed_types:
        raise ValidationError("Only JPEG and PNG images are allowed")
    
    if file.size > max_size:
        raise ValidationError("Image size must be less than 10MB")


class ObjectDetectionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        
        # File validation
        try:
            validate_image_file(image)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        # Save uploaded image
        upload_path = os.path.join(settings.MEDIA_ROOT, image.name)
        with open(upload_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Prepare output path
        annotated_path = os.path.join(settings.MEDIA_ROOT, f"annotated_{image.name}")

        # Run YOLO detection
        detections = detect_objects(upload_path, annotated_path)

        # ✅ SAVE TO DATABASE
        detection_result = DetectionResult.objects.create(
            user=request.user,
            original_image=image,
            annotated_image=f"annotated_{image.name}"
        )
        
        # Save detected objects
        for detection in detections:
            bbox = detection["bbox"]
            DetectedObject.objects.create(
                detection=detection_result,
                class_name=detection["class"],
                confidence=detection["confidence"],
                bbox_x1=bbox[0], bbox_y1=bbox[1],
                bbox_x2=bbox[2], bbox_y2=bbox[3]
            )

        return Response({
            "detection_id": detection_result.id,
            "annotated_image_url": f"/media/annotated_{image.name}",
            "detections": detections,
            "summary": {
                "total_objects": len(detections),
                "unique_classes": list(set(d['class'] for d in detections)),
                "highest_confidence": max(d['confidence'] for d in detections) if detections else 0
            }
        })