from django.db import models

class PdfData(models.Model):
    email = models.EmailField(unique=True)
    content = models.TextField()
    nouns = models.TextField()
    verbs = models.TextField()
