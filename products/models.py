from django.db import models
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField
from app.models import Category,SubCategory,Tag,Type,SubType
from django.core.exceptions import ValidationError

def validate_mp4_extension(value):
    if not value.name.endswith('.mp4'):
        raise ValidationError('Only MP4 files are allowed.')
    
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=False, related_name='cwcategories')
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=False, related_name='cwsubcategories')
    
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, null=True, blank=True, related_name='ptype')
    sub_type = models.ForeignKey(
        SubType, on_delete=models.CASCADE, null=True, blank=True, related_name='psub_type')
    
    name = models.CharField(max_length=255, unique=True,
                            null=True, blank=False)
    slug = models.SlugField(max_length=255,unique=True,null=True, blank=False)
    sub_title=models.CharField(max_length=255,null=True, blank=True,verbose_name="Sub Title")
    shelf_life=models.CharField(max_length=100,null=True, blank=True,verbose_name="Shelf Life")
    
    shelf_life_section_heading=models.CharField(max_length=255,null=True, blank=True)
    shelf_life_section_subheading=models.CharField(max_length=255,null=True, blank=True)
    shelf_life_section_temp_heading=models.CharField(max_length=255,null=True, blank=True)


    storage_temp=models.CharField(max_length=100,null=True, blank=True,verbose_name="Storage Temp")
    background_color_code=models.CharField(max_length=7,null=True,help_text="Ex - #FFFFFF", blank=True,verbose_name="Background Color Code")
    short_description = models.TextField(
        max_length=500, blank=False, null=True,help_text="Short description on listing",)
    description = RichTextUploadingField(null=True, blank=False)
    used_directions = RichTextUploadingField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    shop_now_url = models.URLField(max_length=255, null=True, blank=True)
    meta_title = models.CharField(max_length=255,
                            null=True, blank=True)
    meta_keywords = models.TextField(
        max_length=500, blank=True, null=True)
    meta_description = models.TextField(
        max_length=500, blank=True, null=True)
        
   
    is_active = models.BooleanField(default=True)
    image = ResizedImageField(size=[800, 800], upload_to='products/',
                              verbose_name="List Image", null=True, blank=False, quality=98)
    is_tild_list_image = models.BooleanField(default=False)

    banner_image = ResizedImageField(size=[1000, 1000], upload_to='products/',
                              verbose_name="Banner Image", null=True, blank=True, quality=98)

    video_embed_code = models.TextField(
        max_length=2000, blank=True, null=True)
    video = models.FileField(upload_to='products/', null=True,
                             blank=True,verbose_name="Banner Video", validators=[validate_mp4_extension]) 

    meta_image = ResizedImageField(size=[800, 800], upload_to='metaimage/',
                              verbose_name="Meta Image", null=True, blank=True, quality=98) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)

    heading_for_flavour_section=models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.name
    
class ProductAttributes(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=False, related_name='productattributes')
    heading = models.CharField(
        max_length=100,null=True, blank=False)
    description = RichTextUploadingField(null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('product', 'heading')
    def __str__(self):
        return self.heading

class ProductSize(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=False, related_name='productsize')
    size = models.CharField(
        max_length=100, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('product', 'size')
    def __str__(self):
        return self.size 

class ProductColor(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=False, related_name='productcolor')
    name = models.CharField(
        max_length=50, null=True, blank=False)
    sub_heading = models.CharField(
        max_length=100,null=True, blank=False)
    image = ResizedImageField(size=[800, 800], upload_to='products/',
                              verbose_name="Image", null=True, blank=False, quality=98)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = ('product', 'name','sub_heading')
        verbose_name = "Product Flavour"
        verbose_name_plural = "Product Flavours"
    def __str__(self):
        return self.name

class ProductGalery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=False, related_name='productgalery')
    image = ResizedImageField(size=[800, 800], upload_to='products/',
                              verbose_name="Galery Image", null=True, blank=True, quality=98)
    image_title = models.CharField(
        max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    
                     
