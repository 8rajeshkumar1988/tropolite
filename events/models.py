from django.db import models
from django_resized import ResizedImageField



class Event(models.Model):
    EVENT_TYPES = [
        ('Event', 'Event'),
        ('Exhibition', 'Exhibition'),
    ]
    event_type = models.CharField(
        max_length=10, help_text="Event Type",null=True, blank=False, choices=EVENT_TYPES)
    
    event_name = models.CharField(max_length=255,
                            null=True, blank=False)
    event_date = models.DateField(null=True, blank=False, verbose_name="Event From Date")
    event_to_date = models.DateField(null=True, blank=False,verbose_name="Event End Date")

    slug = models.SlugField(max_length=255,unique=True,null=True, blank=False)
    short_description = models.TextField(
        max_length=500, blank=True, null=True)
   
    is_active = models.BooleanField(default=True)
    image = ResizedImageField(size=[800, 800], upload_to='events/',
                              verbose_name="Cover Image", null=True, blank=False, quality=98)
    
    class Meta:
        unique_together = ('event_type', 'event_name') 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

class EventGallery(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=False, related_name='event_images')
    
    video_embed_code = models.TextField(
        max_length=2000, blank=True, null=True,help_text="Required image or video")
    
    image = ResizedImageField(size=[1200, 1200], upload_to='events/',
                              verbose_name="Galery Image / Video Thumbnail", null=True, blank=False, quality=98)
    image_title = models.CharField(max_length=255,
                            null=True, blank=False)
    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"     

    
    
