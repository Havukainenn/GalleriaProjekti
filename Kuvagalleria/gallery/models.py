from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from PIL import Image as PilImage
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO

class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'
        indexes = [
            models.Index(fields=['user', 'created']),
        ]

    def __str__(self):
        return self.name

class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    description = models.TextField(blank=True, db_index=True)
    folder = models.ForeignKey(Folder, related_name='images', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['folder', 'created']), 
        ]

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            super().save(*args, **kwargs)  
            img = PilImage.open(self.file.path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.thumbnail((300, 300), PilImage.LANCZOS)
            thumb_io = BytesIO()
            img.save(thumb_io, 'JPEG', quality=95)
            thumb_filename = os.path.basename(self.file.name)
            self.thumbnail.save(thumb_filename, ContentFile(thumb_io.getvalue()), save=False)           
        super().save(*args, **kwargs)

@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)
    if instance.thumbnail:
        instance.thumbnail.delete(False)