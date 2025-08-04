from django.contrib import admin
from .models import Category,Tag,Type,CsrCategory,Faq,SubType,CsrReport,CsrHighlight,LeadSource,LeadStatus,Statics,SubCategory,TrustFactor,Customer,Bakery
from django.utils.html import format_html
from django.urls import reverse
from django.utils.html import format_html
import csv
from django.http import HttpResponse
# from django.urls import reverse
# from django.http import HttpResponseRedirect
# from django.contrib.admin.sites import AdminSite

# class CustomAdminSite(AdminSite):
#     def logout(self, request, extra_context=None):
#         # Perform any custom logout logic here if needed
#         # For example, you can log the user's logout activity

#         # Redirect to the login page after logout
#         return HttpResponseRedirect(reverse('admin:login'))
    
# custom_admin_site = CustomAdminSite(name='custom_admin')
# admin.site = custom_admin_site


def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','sequence_number','is_active', 'created_at','preview_link')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')
    prepopulated_fields = {"slug": ("name",)}

    def preview_link(self, obj):
        url = reverse('category', args=[obj.slug])  # Replace 'recipe_detail' with your actual URL name
        return format_html('<a href="{}" target="_blank">Preview</a>', url)

    actions = ['export_selected']

    def export_selected(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="category.csv"'

        writer = csv.writer(response)
        writer.writerow([field.name for field in Category._meta.fields])  # Header row

        for obj in queryset:
            writer.writerow([getattr(obj, field.name) for field in Category._meta.fields])

        return response

    export_selected.short_description = "Export selected items to CSV" 

    def has_delete_permission(self, request, obj=None):
        return False 

admin.site.register(Category, CategoryAdmin)

class TrustFactorAdmin(admin.StackedInline):
    model = TrustFactor
    extra = 0

class TypeAdmin(admin.TabularInline):
    model = Type
    extra = 0 
class SubTypeAdmin(admin.TabularInline):
    model = SubType
    extra = 0       


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('heading','get_category','sequence_number','is_active', 'created_at','preview_link')
    list_filter = (('is_active', customTitledFilter('active')),('category', customTitledFilter('category')))
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')
    prepopulated_fields = {"slug": ("heading",)}

    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = 'category'
    get_category.admin_order_field = 'category__name'

    inlines = [TypeAdmin,SubTypeAdmin,TrustFactorAdmin,]

    def preview_link(self, obj):
        url = reverse('subcategory', args=[obj.category.slug, obj.slug]) # Replace 'recipe_detail' with your actual URL name
        return format_html('<a href="{}" target="_blank">Preview</a>', url)

    actions = ['export_selected']

    def export_selected(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SubCategory.csv"'

        writer = csv.writer(response)
        writer.writerow([field.name for field in SubCategory._meta.fields])  # Header row

        for obj in queryset:
            writer.writerow([getattr(obj, field.name) for field in SubCategory._meta.fields])

        return response

    export_selected.short_description = "Export selected items to CSV" 

    def has_delete_permission(self, request, obj=None):
        return False 

admin.site.register(SubCategory, SubCategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name','sequence_number','slug','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Tag, TagAdmin)


class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('name','sequence_number','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')
    
admin.site.register(LeadSource, LeadSourceAdmin)


class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ('name','sequence_number','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')
    
admin.site.register(LeadStatus, LeadStatusAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','display_image','direction','sequence_number','is_active')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')

    def display_image(self, obj):
            return format_html('<img src="{}" width="65" />', obj.image.url)


    display_image.allow_tags = True
    display_image.short_description = 'Icon'
    
admin.site.register(Customer, CustomerAdmin)

class StaticsAdmin(admin.ModelAdmin):
    list_display = ('heading','value','sequence_number','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')
    
admin.site.register(Statics, StaticsAdmin)

class BakeryAdmin(admin.ModelAdmin):
    list_display = ('name','state','city','pin_code','latitude','longitude','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('is_active',)
    
admin.site.register(Bakery, BakeryAdmin)



class CsrReportAdmin(admin.ModelAdmin):
    list_display = ('heading','display_image','sequence_number','get_csr_category','report_date','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),('csr_category', customTitledFilter('Category')))
    list_per_page = 20  # record 10 per page
    list_editable=('sequence_number','is_active')
    
    def display_image(self, obj):
        if obj.image:
           return format_html('<img src="{}" width="50" height="50" class="popup-image" />', obj.image.url)
        else:
            return ""

    display_image.short_description = 'Image'

    def get_csr_category(self, obj):
        if obj.csr_category:
          return obj.csr_category.name
        else:
          return "N.A" 
    get_csr_category.short_description = 'Category'
    get_csr_category.admin_order_field = 'csr_category__name'      
    
admin.site.register(CsrReport, CsrReportAdmin)

class CsrHighlightAdmin(admin.ModelAdmin):
    list_display = ('heading','display_image','description','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('is_active',)
    def display_image(self, obj):
        if obj.image:
           return format_html('<img src="{}" width="50" height="50" class="popup-image" />', obj.image.url)
        else:
            return ""
    
admin.site.register(CsrHighlight, CsrHighlightAdmin)


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question','answer','is_active')
    list_per_page = 20  # record 10 per page
    #prepopulated_fields = {"slug": ("name",)}
    #list_editable=('sequence_number','is_active')Expedition
admin.site.register(Faq,FaqAdmin)

class CsrCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    list_per_page = 20  # record 10 per page
    #prepopulated_fields = {"slug": ("name",)}
    #list_editable=('sequence_number','is_active')Expedition
admin.site.register(CsrCategory,CsrCategoryAdmin)


