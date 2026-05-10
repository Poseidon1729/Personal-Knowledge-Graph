from django.db import models
from users.models import Users

class Folder(models.Model):
    folder_name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, 
        related_name='subfolders', null=True, blank=True
    )
    owner = models.ForeignKey(
        Users, on_delete=models.CASCADE, 
        related_name='folders'
    )
    allowed_users = models.ManyToManyField(
        Users, related_name='shared_folders', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.folder_name   



