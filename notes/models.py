import os
from django.db import models
from django.conf import settings


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используем AUTH_USER_MODEL
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='note_images/', blank=True, null=True)  # ImageField added
    def delete(self, *args, **kwargs):
        # Удаляем файл изображения, если он есть
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        # Удаляем саму запись
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title