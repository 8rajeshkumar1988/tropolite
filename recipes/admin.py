from django.contrib import admin
from .models import Recipe,Process,ProductFlavourImage,Ingredient,Instruction,Review
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

class ProcessAdmin(admin.StackedInline):
    model = Process
    extra = 0 

class ProductFlavourImageAdmin(admin.StackedInline):
    model = ProductFlavourImage
    extra = 0 


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1



class RecipeAdmin(admin.ModelAdmin):
    list_display = ('full_heading','is_active', 'prep_time','cook_time','preview_link','created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    #list_editable=('sequence_number','is_active')
    prepopulated_fields = {"slug": ("heading","sub_heading")}
    inlines = [IngredientInline,ReviewInline,ProductFlavourImageAdmin,ProcessAdmin]
    search_fields = ['heading', 'sub_heading','slug']

    def full_heading(self, obj):
        return f"{obj.heading} {obj.sub_heading}"
    full_heading.short_description = 'Heading'
    def preview_link(self, obj):
        url = reverse('recipedetail', args=[obj.slug])  # Replace 'recipe_detail' with your actual URL name
        return format_html('<a href="{}" target="_blank">Preview</a>', url)
    
        
    preview_link.short_description = 'Preview Link'
    
    actions = ['export_selected']

    def export_selected(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="recipe.csv"'

        writer = csv.writer(response)
        writer.writerow([field.name for field in Recipe._meta.fields])  # Header row

        for obj in queryset:
            writer.writerow([getattr(obj, field.name) for field in Recipe._meta.fields])

        return response

    export_selected.short_description = "Export selected items to CSV" 

    def has_delete_permission(self, request, obj=None):
        return False 

admin.site.register(Recipe, RecipeAdmin)
