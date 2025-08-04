from django.db import models
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField


class Page(models.Model):
    heading = models.CharField(max_length=255, unique=True,
                            null=True, blank=False)
    slug = models.SlugField(max_length=255,unique=True,null=True, blank=False)
    description = RichTextUploadingField(null=True, blank=True)
    
    meta_title = models.CharField(max_length=255,
                            null=True, blank=True)
    meta_keywords = models.TextField(
        max_length=500, blank=True, null=True)
    meta_description = models.TextField(
        max_length=500, blank=True, null=True)
    meta_image = ResizedImageField(size=[800, 800], upload_to='metaimage/',
                              verbose_name="Meta Image", null=True, blank=True, quality=95) 
    page_schema = models.TextField(blank=True, null=True)
    
   
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading
