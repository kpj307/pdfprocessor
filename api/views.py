from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import PdfData
from .serializers import PdfDataSerializer
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

class PdfUploadView(APIView):
    def post(self, request, format=None):
        file = request.FILES['file']
        email = request.data['email']
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
            # page = pdf_reader.pages[page_num]
            # text += page.extract_text()

        words = word_tokenize(text)
        words = [word for word in words if word.isalnum()]
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.lower() not in stop_words]
        tagged_words = pos_tag(words)
        nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
        verbs = [word for word, pos in tagged_words if pos.startswith('VB')]

        pdf_data = PdfData(email=email, content=text, nouns=" ".join(nouns), verbs=" ".join(verbs))
        pdf_data.save()

        serializer = PdfDataSerializer(pdf_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def extracted_data_view(request):
    data = PdfData.objects.all()
    return render(request, 'extracted_data.html', {'data': data})