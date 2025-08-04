from django.db import models
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError



class JobDepartment(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    sequence_number = models.IntegerField(blank=False, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Job Department"
        verbose_name_plural = "Job Departments"


    def __str__(self):
        return self.name

class Job(models.Model):
    job_department = models.ForeignKey(
        JobDepartment, on_delete=models.CASCADE, null=True, blank=False, related_name='job_departments')
    heading = models.CharField(max_length=255, unique=True,verbose_name="Job Title",
                            null=True, blank=False)
    location = models.CharField(max_length=255,verbose_name="Location",
                            null=True, blank=False)
    job_scope = RichTextUploadingField(null=True, blank=False)
    qualifications = RichTextUploadingField(null=True, blank=False)
    desired_experience_skills = RichTextUploadingField(null=True, blank=True)
    key_Responsibilities = RichTextUploadingField(null=True, blank=True)
    CTC_band = models.CharField(max_length=255,
                            null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading
    
def get_image_filename(instance, filename):
    my_uuid = uuid.uuid4()
    slug = str(my_uuid)
    return "resume/%s-%s" % (slug, filename)

def validate_file_size(value):
    if value.size > 10 * 1024 * 1024:  # 10 MB
        raise models.ValidationError('File size must be no more than 10 MB.')



class JobApply(models.Model):
    STATUS_CHOICES = [
        ("Pending", 'Pending'),
        ("In Progress", 'In Progress'),
        ("On Hold", 'On Hold'),
        ("Rejected", 'Rejected'),
        ("Hired", 'Hired'),
    ]
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, null=True, blank=False, related_name='jobs')
    name = models.CharField(max_length=50,null=True, blank=False)
    work_experience = models.CharField(max_length=50,null=True, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=False)
    mobile = models.CharField(max_length=10, null=True, blank=False)
    qualification = models.CharField(max_length=100,null=True, blank=False)
    current_location = models.CharField(max_length=50,null=True, blank=False)
    preferred_location = models.CharField(max_length=50,null=True, blank=False)
    resume = models.FileField(
        upload_to=get_image_filename, null=True, blank=False, verbose_name='Resume',validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docs','docx']),
            validate_file_size,  # Custom validator for file size
        ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    #cover_letter = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return self.name
    
    def get_extension(self):
        resume, extension = os.path.splitext(self.resume.name)
        return extension
