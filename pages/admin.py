from django.contrib import admin
from .models import Page
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


class PageAdmin(admin.ModelAdmin):
    list_display = ('heading','is_active', 'created_at','preview_link')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    #list_editable=('sequence_number','is_active')
    prepopulated_fields = {"slug": ("heading",)}

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
