from django.urls import path
from .views import FrameUploadView

urlpatterns = [
    path('upload-detection/', FrameUploadView.as_view(), name='upload-detection'),
]
