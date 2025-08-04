from django.contrib import admin
from .models import Product,ProductAttributes,ProductSize,ProductColor,ProductGalery
from django.utils.html import format_html
from .forms import ProductForm
from django.urls import reverse
from django.http import HttpResponse
import csv



def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class ProductAttributesAdmin(admin.StackedInline):
    model = ProductAttributes
    extra = 0

class ProductSizeAdmin(admin.StackedInline):
    model = ProductSize
    extra = 0

class ProductColorAdmin(admin.StackedInline):
    model = ProductColor
    extra = 0

class ProductGaleryAdmin(admin.StackedInline):
    model = ProductGalery
    extra = 0 


class ProductAdmin(admin.ModelAdmin):
    form=ProductForm
    list_display = ('name','display_image','get_category','get_subcategory','is_active', 'created_at','preview_link')
    list_filter = (('is_active', customTitledFilter('active')),('category', customTitledFilter('category')),('subcategory', customTitledFilter('subcategory')),('type', customTitledFilter('type')),('sub_type', customTitledFilter('sub_type')))
    list_per_page = 20  # record 10 per page
    list_editable=('is_active',)
    prepopulated_fields = {"slug": ("name",)}
    #change_list_template = "admin/products/product/image_list_display_popup.html"
    search_fields = ['name',]
    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = 'category'
    get_category.admin_order_field = 'category__name'

    def get_subcategory(self, obj):
        return obj.subcategory.heading
    get_subcategory.short_description = 'subcategory'
    get_subcategory.admin_order_field = 'subcategory__heading'

    def display_image(self, obj):
        if obj.image:
            image_url = obj.image.url
        else:
            # If the image field is empty, use a placeholder image
            image_url = '/static/path/to/your/default/image.png'

        image_tag = format_html('<img src="{}" width="50" height="50" class="popup-image" />', image_url)
        return format_html('<a href="#" class="popup-link" data-image-url="{}">{}</a>', image_url, image_tag)

    display_image.short_description = 'Image'

    def preview_link(self, obj):
        url = reverse('productdetail', args=[obj.category.slug, obj.subcategory.slug, obj.slug])  # Replace 'recipe_detail' with your actual URL name
        return format_html('<a href="{}" target="_blank">Preview</a>', url)

    inlines = [ProductAttributesAdmin,ProductSizeAdmin,ProductColorAdmin,ProductGaleryAdmin]
    class Media:
        js = ("js/popup.js",)


    actions = ['export_selected']

    def export_selected(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="product.csv"'

        writer = csv.writer(response)
        writer.writerow([field.name for field in Product._meta.fields])  # Header row

        for obj in queryset:
            writer.writerow([getattr(obj, field.name) for field in Product._meta.fields])

        return response

    export_selected.short_description = "Export selected items to CSV"   

    def has_delete_permission(self, request, obj=None):
        return False  

admin.site.register(Product, ProductAdmin)