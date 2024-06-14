from django.shortcuts import render, redirect
from .forms import PdfUploadForm
from .models import PdfData
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def upload_view(request):
    if request.method == 'POST':
        form = PdfUploadForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            file = form.cleaned_data['file']

            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            # for page_num in range(len(pdf_reader.pages)):
            #     text += pdf_reader.pages[page_num].extract_text()

            words = word_tokenize(text)
            words = [word for word in words if word.isalnum()]
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word.lower() not in stop_words]
            tagged_words = pos_tag(words)
            nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
            verbs = [word for word, pos in tagged_words if pos.startswith('VB')]

            pdf_data = PdfData(email=email, content=text, nouns=" ".join(nouns), verbs=" ".join(verbs))
            pdf_data.save()
            return redirect('extracted-data')
    else:
        form = PdfUploadForm()
    return render(request, 'upload.html', {'form': form})

def extracted_data_view(request):
    data = PdfData.objects.all()
    return render(request, 'extracted_data.html', {'data': data})
