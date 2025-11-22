from django.db import models
from django.contrib.auth.models import User

class DetectionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='uploads/')
    annotated_image = models.ImageField(upload_to='annotated/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Detection {self.id} by {self.user.username}"

class DetectedObject(models.Model):
    detection = models.ForeignKey(DetectionResult, on_delete=models.CASCADE, related_name='detected_objects')
    class_name = models.CharField(max_length=100)
    confidence = models.FloatField()
    bbox_x1 = models.IntegerField()
    bbox_y1 = models.IntegerField()
    bbox_x2 = models.IntegerField()
    bbox_y2 = models.IntegerField()
    
    class Meta:
        ordering = ['-confidence']