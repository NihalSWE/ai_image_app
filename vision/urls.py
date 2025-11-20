from django.urls import path
from .views import ObjectDetectionView

urlpatterns = [
    path('', ObjectDetectionView.as_view(), name='object-detection'),
]
