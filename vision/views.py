from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageUploadSerializer
from .utils import detect_objects
import os
from django.conf import settings

class ObjectDetectionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']

        # Save uploaded image
        upload_path = os.path.join(settings.MEDIA_ROOT, image.name)
        with open(upload_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Prepare output path
        annotated_path = os.path.join(settings.MEDIA_ROOT, f"annotated_{image.name}")

        # Run YOLO detection
        detections = detect_objects(upload_path, annotated_path)

        return Response({
            "annotated_image_url": f"/media/annotated_{image.name}",
            "detections": detections
        })
