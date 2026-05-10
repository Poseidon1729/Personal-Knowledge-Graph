from django.db import models
from ui.models import Folder
from django.conf import settings

class File(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='media/', default=None)
    folder = models.ManyToManyField(Folder,blank=True, related_name="files")
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name or self.file.name or f"File {self.pk}"

class Excerpt(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    document = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

