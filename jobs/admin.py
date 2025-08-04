from django.contrib import admin

from .models import Job,JobApply,JobDepartment


def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class JobDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),)
    list_per_page = 20  # record 10 per page
    #list_editable=('sequence_number','is_active')
    
admin.site.register(JobDepartment, JobDepartmentAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ('heading','get_job_department','is_active', 'created_at')
    list_filter = (('is_active', customTitledFilter('active')),('job_department', customTitledFilter('Department')))
    list_per_page = 20  # record 10 per page
    

    def get_job_department(self, obj):
        if obj.job_department:
          return obj.job_department.name
        else:
          return "N.A"  
    get_job_department.short_description = 'Department'
    get_job_department.admin_order_field = 'job_department__name' 

    
admin.site.register(Job, JobAdmin)


class JobApplyAdmin(admin.ModelAdmin):
    list_display = ('name','work_experience','email','mobile','qualification','current_location','preferred_location','created_at','status')
    list_filter = (('job', customTitledFilter('job')),('status', customTitledFilter('status')),('created_at', customTitledFilter('Received At')))
    list_per_page = 20  # record 10 per page
    search_fields = ['name', 'mobile', 'email']
    list_editable=('status',)
    readonly_fields = ['job','name','work_experience','email','mobile','qualification','current_location','preferred_location','resume']
    def has_delete_permission(self, request, obj=None):
        return False  
    
    def has_add_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False  
    
admin.site.register(JobApply, JobApplyAdmin)