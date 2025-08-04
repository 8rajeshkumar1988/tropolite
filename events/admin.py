from django.contrib import admin
from .models import Event,EventGallery
from django.utils.html import format_html

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class EventGalleryAdmin(admin.StackedInline):
    model = EventGallery
    extra = 0 

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name','event_date','event_to_date','event_type','is_active','display_image', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
   
    prepopulated_fields = {"slug": ("event_name",)}
    
    def display_image(self, obj):
        if obj.image:
            image_url = obj.image.url
            return format_html('<img src="{}" width="50" height="50" class="popup-image" />', image_url)
        else:
            return None
        

    display_image.short_description = 'Cover Image'
    inlines = [EventGalleryAdmin,]

admin.site.register(Event, EventAdmin) 
