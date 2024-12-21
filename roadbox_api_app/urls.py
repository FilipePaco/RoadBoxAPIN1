from django.urls import path
from .views import *

urlpatterns = [
    path('upload-detection/', FrameUploadView.as_view(), name='upload-detection'),
    path('upload-camera/', Camera.as_view(), name='upload-camera'),
]
