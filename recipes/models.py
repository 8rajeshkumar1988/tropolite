from django.db import models
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField
from app.models import Tag
from products.models import Product
from django.core.exceptions import ValidationError

def validate_mp4_extension(value):
    if not value.name.endswith('.mp4'):
        raise ValidationError('Only MP4 files are allowed.')

class Recipe(models.Model):
    heading = models.CharField(max_length=255,
                            null=True, blank=False)
    
    sub_heading = models.CharField(max_length=255,
                            null=True, blank=True)
    slug = models.SlugField(max_length=255,unique=True,null=True, blank=False)
    description = RichTextUploadingField(
        null=True, blank=True, verbose_name="Left Description")
    right_description = RichTextUploadingField(
        null=True, blank=True, verbose_name="Right Description")

    how_to_make_it =  RichTextUploadingField(
        null=True, blank=False, verbose_name="Product Short Description")
    
    bottom_description_heading = models.CharField(max_length=255,
                            null=True, blank=True)
    bottom_description = RichTextUploadingField(
        null=True, blank=True, verbose_name="Bottom Left Description") 
    
    bottom_right_description = RichTextUploadingField(
        null=True, blank=True, verbose_name="Bottom Right Description") 

    prep_time = models.CharField(max_length=50,
                            null=True, blank=True)
    
    cook_time=models.CharField(max_length=50,
                            null=True, blank=True,help_text="PT1H or PT15M")
    person_served = models.PositiveIntegerField(null=True, blank=True)
    ingredients_used = models.PositiveIntegerField(null=True, blank=True)
    


    written_by = models.CharField(max_length=50,
                            null=True, blank=True,verbose_name="Author")
    meta_title = models.CharField(max_length=255,
                            null=True, blank=True)
    meta_keywords = models.TextField(
        max_length=500, blank=True, null=True)
    meta_description = models.TextField(
        max_length=500, blank=True, null=True)
        
    products = models.ManyToManyField(Product, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = ResizedImageField(size=[800, 800], upload_to='recipes/',
                              verbose_name="List Image", null=True, blank=True, quality=95)
    
    banner_image = ResizedImageField(upload_to='recipes/',
                              verbose_name="Banner Image", null=True, blank=True, quality=95)
    
    video = models.FileField(upload_to='videos/', null=True, blank=True, validators=[validate_mp4_extension])
    meta_image = ResizedImageField(size=[800, 800], upload_to='metaimage/',
                              verbose_name="Meta Image", null=True, blank=True, quality=95)

    canonical_url=models.CharField(max_length=255,
                            null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading
    
    class Meta:
        unique_together = ('heading', 'sub_heading')
    


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.quantity} of {self.name}'

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveIntegerField()
    text = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f'Step {self.step_number} for {self.recipe.title}'

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=255)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} for {self.recipe.title}'



class ProductFlavourImage(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=True, blank=False, related_name='recipefl')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=False, related_name='recipeproduct')
    image = ResizedImageField(size=[800, 800], upload_to='products/',
                              verbose_name="List Image", null=True, blank=False, quality=98)
    



class Process(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=True, blank=False, related_name='recipeprocess')
    image = ResizedImageField(size=[800, 800], upload_to='recipes/',
                              verbose_name="Galery Image", null=True, blank=True, quality=95)
    description = RichTextUploadingField(
        null=True, blank=False, verbose_name="Description")
    sequence_number = models.IntegerField(blank=False, default=1, null=True)