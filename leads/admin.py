from django.contrib import admin
from .models import Lead,Reminders,Notes,EmailTemplate,SendEmail,EmailTracking,Campaign,CampaignTracking
from django.http import HttpResponse
import csv
from .utils import send_mail

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper




class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_name','utm_source','utm_medium', 'utm_campaign','created_at','is_active')
    list_per_page = 20  # record 10 per page
admin.site.register(Campaign, CampaignAdmin)



class CampaignTrackingAdmin(admin.ModelAdmin):
    list_display = ('campaign','get_utm_source','get_utm_medium','get_utm_campaign','ip_address','user_agent', 'created_at')
    list_per_page = 20  # record 10 per page
    search_fields = ['campaign__utm_source','campaign__utm_medium','campaign__utm_campaign','campaign__campaign_name']
    
    list_filter = (('campaign', customTitledFilter('Campaign')),('created_at', customTitledFilter('created at')))

    def get_utm_source(self, obj):
        return obj.campaign.utm_source
    get_utm_source.short_description = 'utm source'
    get_utm_source.admin_order_field = 'campaign__utm_source'

    def get_utm_medium(self, obj):
        return obj.campaign.utm_medium
    get_utm_medium.short_description = 'utm medium'
    get_utm_medium.admin_order_field = 'campaign__utm_medium'

    def get_utm_campaign(self, obj):
        return obj.campaign.utm_campaign
    get_utm_campaign.short_description = 'utm campaign'
    get_utm_campaign.admin_order_field = 'campaign__utm_campaign'
    

    def has_delete_permission(self, request, obj=None):
        return False 
    
    def has_add_permission(self, request, obj=None):
        # Disable delete
        return False

    def has_change_permission(self, request, obj=None):
        # Disable delete
        return False  
admin.site.register(CampaignTracking, CampaignTrackingAdmin)

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name','subject', 'created_at')
    list_per_page = 20  # record 10 per page
admin.site.register(EmailTemplate, EmailTemplateAdmin)



class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ('send_email','ip_address','user_agent', 'created_at')
    list_per_page = 20  # record 10 per page
    search_fields = ['send_email__email_to', ]
    
   
    
    def has_delete_permission(self, request, obj=None):
        return False 
    
    def has_add_permission(self, request, obj=None):
        # Disable delete
        return False

    def has_change_permission(self, request, obj=None):
        # Disable delete
        return False  
admin.site.register(EmailTracking, EmailTrackingAdmin)

class SendEmailAdmin(admin.ModelAdmin):
    list_display = ('email_template','email_to','is_opened', 'created_at')
    list_per_page = 20  # record 10 per page
    readonly_fields = ['tracking_id','is_opened','opened_at']
    
    def save_model(self, request, obj, form, change):
       super().save_model(request, obj, form, change)
       send_mail(obj.id)
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    
    # def has_add_permission(self, request, obj=None):
    #     # Disable delete
    #     return False

    def has_change_permission(self, request, obj=None):
        # Disable delete
        return False  


admin.site.register(SendEmail, SendEmailAdmin)


class RemindersAdmin(admin.TabularInline):
    model = Reminders
    extra = 0
    #list_display = ('date_to_be_notified','reminder_to','description')
    #readonly_fields = ['date_to_be_notified', 'reminder_to','description']
    #template = 'admin/leads/edit_button_inline.html'
    
class NotesAdmin(admin.TabularInline):
    model = Notes
    extra = 0
    #list_display = ('date_to_be_notified','reminder_to','description')
    #readonly_fields = ['date_to_be_notified', 'reminder_to','description']
    #template = 'admin/leads/edit_button_inline.html'    

class LeadAdmin(admin.ModelAdmin):
    list_display = ('name','mobile','email','description','zip_code','city','state','get_product','created_at','lead_status')
    #list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    list_editable=('lead_status',)
    inlines = [RemindersAdmin,NotesAdmin]
   
    list_filter = (('lead_status', customTitledFilter('Lead Status')),('product', customTitledFilter('product')),('created_at', customTitledFilter('created at')))
    #actions = ['mark_as_junk_selected', 'mark_as_lost_selected']#'delete_selected', 
    search_fields = ['name', 'mobile', 'email','zip_code']
    # def delete_selected(self, request, queryset):
    #     queryset.update(is_deleted=True)
    # delete_selected.short_description = "Delete Selected"
    exclude = ('is_deleted',) 
    # def mark_as_junk_selected(self, request, queryset):
    #     queryset.update(is_junk=True)
    # mark_as_junk_selected.short_description = "Mark as Junk"

    # def mark_as_lost_selected(self, request, queryset):
    #     queryset.update(is_lost=True)
    # mark_as_lost_selected.short_description = "Mark as Lost"

    def has_delete_permission(self, request, obj=None):
        return False 

    def get_product(self, obj):
        if obj.product:
           return obj.product.name
        else:
            return "General Enquiry"
    get_product.short_description = 'product'
    get_product.admin_order_field = 'product__name'

    actions = ['export_selected']

    def export_selected(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'

        writer = csv.writer(response)
        writer.writerow([field.name for field in Lead._meta.fields])  # Header row

        for obj in queryset:
            writer.writerow([getattr(obj, field.name) for field in Lead._meta.fields])

        return response

    export_selected.short_description = "Export selected items to CSV"



admin.site.register(Lead, LeadAdmin)
#admin.site.register(Reminders)