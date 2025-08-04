from django.db import models
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError


def validate_mp4_extension(value):
    if not value.name.endswith('.mp4'):
        raise ValidationError('Only MP4 files are allowed.')


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            null=True, blank=False)
    heading = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    description_heading = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(
        null=True, blank=False, verbose_name="Left Description")
    right_description = RichTextUploadingField(
        null=True, blank=True, verbose_name="Right Description")

    banner_video_embed_code = models.TextField(
        max_length=2000, blank=True, null=True)
    
    banner_video = models.FileField(upload_to='category/', null=True, help_text="Required banner image or banner video",
                                    verbose_name="Banner Video", blank=True, validators=[validate_mp4_extension])
    banner_image = ResizedImageField(size=[1600, 800], upload_to='category/',
                                     verbose_name="Banner Image", help_text="Required banner image or banner video", null=True, blank=True, quality=95)

    subcategory_sec_heading = models.CharField(max_length=255, null=True, blank=True)
    subcategory_sec_subheading = models.CharField(max_length=255, null=True, blank=True)
    subcategory_sec_short_des = models.TextField(
        max_length=500, blank=True, null=True)
  
    bootom_image = ResizedImageField(size=[800, 800], upload_to='category/',
                                    null=True, blank=True, quality=95)
    bootom_description = RichTextUploadingField(
        null=True, blank=True)
    
    meta_title = models.CharField(max_length=255,
                                  null=True, blank=True)
    meta_keywords = models.TextField(
        max_length=500, blank=True, null=True)
    meta_description = models.TextField(
        max_length=500, blank=True, null=True)
    meta_image = ResizedImageField(size=[800, 800], upload_to='metaimage/',
                                   verbose_name="Meta Image", null=True, blank=True, quality=95)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=False, related_name='categories')
    heading = models.CharField(
        max_length=100, unique=True, null=True, blank=False)
    slug = models.SlugField(max_length=255)
    sub_title = models.CharField(max_length=255, null=True, blank=True)
    short_description = RichTextUploadingField(
        null=True, blank=False, verbose_name="List Description")
    description = RichTextUploadingField(
        null=True, blank=False, verbose_name="Intro Description")

    product_section_heading = models.CharField(
        max_length=255, null=True, blank=True)
    product_section_subtitle = models.CharField(max_length=255, null=True, blank=True)

    product_section_content = RichTextUploadingField(
        null=True, blank=True)

    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    meta_title = models.CharField(max_length=255,
                                  null=True, blank=True)
    meta_keywords = models.TextField(
        max_length=500, blank=True, null=True)
    meta_description = models.TextField(
        max_length=500, blank=True, null=True)

    meta_image = ResizedImageField(size=[800, 800], upload_to='metaimage/',
                                   verbose_name="Meta Image", null=True, blank=True, quality=95)

    list_image = ResizedImageField(size=[800, 800], upload_to='category/',
                                   verbose_name="List Image", null=True, blank=True, quality=95)

    banner_image = ResizedImageField(size=[800, 1600], upload_to='category/',
                                     verbose_name="Banner Image", null=True, blank=True, quality=95)

    video_embed_code = models.TextField(
        max_length=2000, blank=True, null=True)
    video = models.FileField(upload_to='category/', null=True,
                             blank=True, validators=[validate_mp4_extension])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.heading



class Type(models.Model):
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=False, related_name='subcat_types')
    name = models.CharField(max_length=100, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    class Meta:
        unique_together = ('subcategory', 'name')

    def __str__(self):
        return self.name

class SubType(models.Model):
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=False, related_name='subcat_subtypes')
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, null=True, blank=False, related_name='subcat_types_sub')
    name = models.CharField(max_length=100, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    class Meta:
        unique_together = ('subcategory', 'name')

    def __str__(self):
        return self.name


class TrustFactor(models.Model):
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=False, related_name='tfsubcategory')
    heading = models.CharField(max_length=100, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    image = ResizedImageField(size=[800, 800], upload_to='category/',
                              verbose_name="Icon", null=True, blank=True, quality=95)

    class Meta:
        unique_together = ('subcategory', 'heading')

    def __str__(self):
        return self.heading


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            null=True, blank=False)
    slug = models.SlugField(max_length=255)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LeadSource(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LeadStatus(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Statics(models.Model):
    heading = models.CharField(
        max_length=100, unique=True, null=True, blank=False)
    value = models.CharField(max_length=100, null=True, blank=False)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Legacy Number"
        verbose_name_plural = "Legacy Numbers"
    def __str__(self):
        return self.heading


class Customer(models.Model):
    DIRECTION_CHOICES = [
        ('right', 'Right'),
        ('left', 'Left'),
    ]
    direction = models.CharField(
        max_length=10, help_text="Icon movement direction", choices=DIRECTION_CHOICES)
    name = models.CharField(max_length=100, null=True, blank=False)
    image = ResizedImageField(size=[800, 800], upload_to='category/',
                              verbose_name="Icon", null=True, blank=False, quality=95)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('direction', 'name')

    def __str__(self):
        return self.name


class Bakery(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=False)
    contact_no = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('state', 'name','city','pin_code')
        verbose_name = "Tropolite Dealer"
        verbose_name_plural = "Tropolite Dealers" 
    def __str__(self):
        return self.name
    

class CsrHighlight(models.Model):
    heading = models.CharField(max_length=100, null=True, blank=False)
    description = models.TextField(
        max_length=1000, blank=False, null=True)
    image = ResizedImageField(size=[1600, 800], upload_to='category/',
                              verbose_name="Image", null=True, blank=False, quality=95)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CSR Highlight"
        verbose_name_plural = "CSR Highlights"

    def __str__(self):
        return self.heading 
    

class CsrCategory(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            null=True, blank=False)
    icon = models.FileField(upload_to='category/')
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "CSR Category"
        verbose_name_plural = "CSR Categories"

    def __str__(self):
        return self.name    

class CsrReport(models.Model):
    csr_category = models.ForeignKey(
        CsrCategory, on_delete=models.CASCADE, null=True, blank=False, related_name='csr_categories')
    heading = models.CharField(max_length=100, null=True, blank=False)
    report_date = models.DateField(blank=False, null=True)
    image = ResizedImageField(size=[1600, 800], upload_to='category/',
                              verbose_name="Image", null=True, blank=False, quality=95)
    
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('csr_category','heading', 'report_date')
        verbose_name = "CSR Report"
        verbose_name_plural = "CSR Reports"

    def __str__(self):
        return self.heading   

class Faq(models.Model):
    question =  models.TextField(blank=False, null=True)
    answer =  models.TextField(blank=False, null=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

