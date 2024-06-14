from django.urls import path
from .views import upload_view, extracted_data_view

urlpatterns = [
    path('', upload_view, name='upload'),
    path('extracted-data/', extracted_data_view, name='extracted-data'),
]
