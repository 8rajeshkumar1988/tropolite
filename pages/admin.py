from django.contrib import admin
from .models import Page,Leadership,LeadershipGroupImage,AboutUsImage,OurBrand,CarrerImage,CsrImage,PatentsCertificatesImage,FoodDairyTechnologyImage,MicrobialBiotechnologyImage
from django.urls import reverse
from django.utils.html import format_html
import csv
from django.http import HttpResponse


def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class LeadershipAdmin(admin.StackedInline):
    model = Leadership
    extra = 0 


class LeadershipGroupImageAdmin(admin.StackedInline):
    model = LeadershipGroupImage
    extra = 0 
    max_num = 1


class AboutUsImageAdmin(admin.StackedInline):
    model = AboutUsImage
    extra = 0 
    max_num = 1   
class OurBrandAdmin(admin.StackedInline):
    model = OurBrand
    extra = 0 
   
class CarrerImageAdmin(admin.StackedInline):
    model = CarrerImage
    extra = 1
    max_num = 1   


class CsrImageAdmin(admin.StackedInline):
    model = CsrImage
    extra = 1
    max_num = 1  

class PatentsCertificatesImageAdmin(admin.StackedInline):
    model = PatentsCertificatesImage
    extra = 1
    max_num = 1  

class FoodDairyTechnologyImageAdmin(admin.StackedInline):
    model = FoodDairyTechnologyImage
    extra = 1
    max_num = 1 


class MicrobialBiotechnologyImageAdmin(admin.StackedInline):
    model = MicrobialBiotechnologyImage
    extra = 1
    max_num = 1 

    

class PageAdmin(admin.ModelAdmin):
    list_display = ('heading','is_active', 'created_at','preview_link')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    #list_editable=('sequence_number','is_active')
    prepopulated_fields = {"slug": ("heading",)}
    inlines = [LeadershipAdmin,LeadershipGroupImageAdmin,AboutUsImageAdmin,OurBrandAdmin,CarrerImageAdmin,CsrImageAdmin,PatentsCertificatesImageAdmin,FoodDairyTechnologyImageAdmin,MicrobialBiotechnologyImageAdmin]

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)

        if obj and obj.id == 3:
            # Only show LeadershipAdmin
            return [inline for inline in inline_instances if isinstance(inline,(LeadershipAdmin, LeadershipGroupImageAdmin))]
        elif obj and obj.id == 2:
            # Only show LeadershipAdmin
            return [inline for inline in inline_instances if isinstance(inline,(AboutUsImageAdmin,OurBrandAdmin))]
        elif obj and obj.id == 11:
            # Only show LeadershipAdmin
            return [inline for inline in inline_instances if isinstance(inline,(CarrerImageAdmin))]
        elif obj and obj.id == 12:
            # Only show LeadershipAdmin
            return [inline for inline in inline_instances if isinstance(inline,(CsrImageAdmin))]
        elif obj and obj.id == 14:
            # Only show LeadershipAdmin
            return [inline for inline in inline_instances if isinstance(inline,(PatentsCertificatesImageAdmin))]
        
        elif obj and obj.id == 5:
            # Only show LeadershipAdmin
            return [inline for inline in inline_instances if isinstance(inline,(FoodDairyTechnologyImageAdmin))]
        elif obj and obj.id ==15:
            # Only show LeadershipAdmin
            return [inline for inline in inline_instances if isinstance(inline,(MicrobialBiotechnologyImageAdmin))]
        
        else: 
            # Only show OtherInfo
            return []

    def preview_link(self, obj):
        url = "/"+obj.slug  # Replace 'recipe_detail' with your actual URL name
        return format_html('<a href="{}" target="_blank">Preview</a>', url)
    

    actions = ['export_selected']

    def export_selected(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="page.csv"'

        writer = csv.writer(response)
        writer.writerow([field.name for field in Page._meta.fields])  # Header row

        for obj in queryset:
            writer.writerow([getattr(obj, field.name) for field in Page._meta.fields])

        return response

    export_selected.short_description = "Export selected items to CSV" 

    def has_delete_permission(self, request, obj=None):
        return False 
admin.site.register(Page, PageAdmin)
