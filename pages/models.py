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
    



class Leadership(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_leadership')
    name = models.CharField(max_length=255,
                            null=True, blank=False)
    position = models.CharField(max_length=255,
                            null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=False)
    image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    image_alt_text = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class LeadershipGroupImage(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_leadershipgimg')
    image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Leaders Group Image"
        verbose_name_plural = "Leaders Group Image"
    

    def __str__(self):
        return self.image_alt_text    
    

class AboutUsImage(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_aboutus')
    top_video_iframe=models.TextField(null=True, blank=True)
    who_we_are=models.ImageField(upload_to='leadership/',null=True, blank=True)
    who_we_are_alt_text = models.CharField(max_length=255, null=True, blank=True)

    our_vision=models.ImageField(upload_to='leadership/',null=True, blank=True)
    our_vision_alt_text = models.CharField(max_length=255, null=True, blank=True)

    our_mission=models.ImageField(upload_to='leadership/',null=True, blank=True)
    our_mission_alt_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "About Us Image"
        verbose_name_plural = "About Us Images"
    

    # def __str__(self):
    #     return self.image_alt_text   





class OurBrand(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_ourbrands')
    
    description = models.TextField(max_length=255,
                            null=True, blank=True)
    
    image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    image_alt_text = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.name


class CarrerImage(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_career')
    top_video_iframe=models.TextField(null=True, blank=True)

    cultivating_creativity_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    cultivating_creativity_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    cultivating_leadership_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    cultivating_leadership_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    opportunities_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    opportunities_image_alt_text = models.CharField(max_length=255, null=True, blank=True)


    diversity_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    diversity_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Carrer Image"
        verbose_name_plural = "Carrer Images"
    

    # def __str__(self):
    #     return self.image_alt_text      
    # 
    # 
    #  


class CsrImage(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_csr')
    

    top_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    top_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

  


    CSR_objective_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    CSR_objective_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "CSR Page Image"
        verbose_name_plural = "CSR Page Images"



class PatentsCertificatesImage(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_patentscertificates')
    top_video_iframe=models.TextField(null=True, blank=True)

    quality_and_safety_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    quality_and_safety_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    our_patents_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    our_patents_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    

    class Meta:
        verbose_name = "Patents Certificates Image"
        verbose_name_plural = "Patents Certificates Images"




class FoodDairyTechnologyImage(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_pfdt')
    top_video_iframe=models.TextField(null=True, blank=True)

    formulating_the_future_of_flavor_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    formulating_the_future_of_flavor_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    redefining_bakery_artistry_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    redefining_bakery_artistry_image_alt_text = models.CharField(max_length=255, null=True, blank=True)


    unleashing_taste_and_texture_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    unleashing_taste_and_texture_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    r_and_d_activities_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    r_and_d_activities_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    

    class Meta:
        verbose_name = "Food & Dairy Technology Image"
        verbose_name_plural = "Food & Dairy Technology Images"




class MicrobialBiotechnologyImage(models.Model):
    page=models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=False, related_name='page_mb')
    top_video_iframe=models.TextField(null=True, blank=True)

    art_of_fermentation_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    art_of_fermentation_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    championing_progress_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    championing_progress_image_alt_text = models.CharField(max_length=255, null=True, blank=True)


    exploring_health_benefits_image=models.ImageField(upload_to='leadership/',null=True, blank=True)
    exploring_health_benefits_image_alt_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Microbial Biotechnology Image"
        verbose_name_plural = "Microbial Biotechnology Images"
    