from django.db import models
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField
from app.models import Tag
from products.models import Product

class Blog(models.Model):
    heading = models.CharField(max_length=255,
                            null=True, blank=False)
    
    sub_heading = models.CharField(max_length=255,null=True, blank=True)
    slug = models.SlugField(max_length=255,unique=True,null=True, blank=False)
    intro_description = RichTextUploadingField(null=True, blank=True) 
    
    description = RichTextUploadingField(null=True, blank=False)
    written_by = models.CharField(max_length=50,
                            null=True, blank=True)
    products = models.ManyToManyField(Product, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    meta_title = models.CharField(max_length=255,
                            null=True, blank=True)
    meta_keywords = models.TextField(
        max_length=500, blank=True, null=True)
    meta_description = models.TextField(
        max_length=500, blank=True, null=True)
   
    is_active = models.BooleanField(default=True)
    image = ResizedImageField(size=[800, 800], upload_to='blogs/',
                              verbose_name="List Image", null=True, blank=True, quality=95)
    
    banner_image = ResizedImageField(upload_to='blogs/',
                              verbose_name="Banner Image", null=True, blank=True, quality=95)
    
    meta_image = ResizedImageField(size=[800, 800], upload_to='metaimage/',
                                   verbose_name="Meta Image", null=True, blank=True, quality=95)
    
    canonical_url=models.TextField(max_length=255,
                            null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading
    
    class Meta:
        unique_together = ('heading', 'sub_heading')
