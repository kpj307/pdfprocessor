from django.urls import path
from .views import PdfUploadView, extracted_data_view
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', PdfUploadView.as_view(), name='pdf-upload'),
    path('', TemplateView.as_view(template_name='upload.html')),
    path('extracted-data/', extracted_data_view, name='extracted-data'),
]
