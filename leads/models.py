from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from app.models import Category, SubCategory, LeadStatus
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField


class Lead(models.Model):
    name = models.CharField(max_length=50, default="", null=True, blank=False)
    mobile = models.CharField(max_length=10, null=True, blank=False)
    email = models.EmailField(
        max_length=255, null=True, default="", blank=False)
    description = models.TextField(
        max_length=500, default="", null=True, blank=False, verbose_name="Query")
    # address = models.CharField(max_length=255, default="", null=True, blank=True)
    city = models.CharField(max_length=50, default="", null=True, blank=True)
    state = models.CharField(max_length=50, default="", null=True, blank=True)
    zip_code = models.CharField(
        max_length=6, default="", null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True, related_name='leadcategories')
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='leadsubcategories')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True, related_name='leadproducts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    lead_status = models.ForeignKey(
        LeadStatus, on_delete=models.CASCADE, null=True, default=1, related_name='enquirystatus', blank=True)

    def __str__(self):
        return self.name


class Reminders(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, null=True, blank=False, related_name='leads')
    date_to_be_notified = models.DateTimeField(null=True, blank=False)
    reminder_to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='reminders_users')
    description = models.CharField(
        max_length=500, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lead.name+" "+str(self.date_to_be_notified)


class Notes(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, null=True, blank=False, related_name='lead_notes')
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=False, related_name='notes_users')
    note = models.TextField(max_length=500, default="", null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lead.name+" "+self.added_by.first_name


class Campaign(models.Model):
    campaign_name = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        unique=True
    )
    utm_source = models.CharField(max_length=100,
                                  null=True, blank=False, help_text='Identifies which site sent the traffic, example:google')
    utm_medium = models.CharField(max_length=100,
                                  null=True, blank=False, help_text='Identifies what type of link was used, such as Pay-per-click or email, example:ppc')
    utm_campaign = models.CharField(max_length=100,
                                    null=True, blank=False, help_text='Identifies a specific product promotion or strategic campaign, example:spring_sale')
   
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utm_source', 'utm_medium','utm_campaign')

    def __str__(self):
        return self.campaign_name

class CampaignTracking(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name='campaign_tracking',

    )
    ip_address = models.CharField(
        max_length=255,
        null=True,
        blank=False,
    )
    user_agent = models.CharField(
        max_length=500,  # Adjust the max length as needed
        null=True,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True)
    
    class Meta:
        verbose_name = "Campaign Tracking"
        verbose_name_plural = "Campaign Trackings"

    def __str__(self):
        return self.ip_address    


class EmailTemplate(models.Model):
    template_name = models.CharField(max_length=255,
                                     null=True, blank=False, unique=True)
    subject = models.CharField(max_length=255,
                               null=True, blank=False)
    email_body = RichTextUploadingField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mail Template"
        verbose_name_plural = "Mail Templates"

    def __str__(self):
        return self.template_name


class SendEmail(models.Model):
    email_template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name='email_template',
        help_text='Select the email template you want to use for this email.'
    )
    send_to_name = models.CharField(
        max_length=25,
        null=True,
        blank=False,
    )
    email_to = models.EmailField(
        null=True,
        blank=False,
    )
    email_cc = models.TextField(
        null=True,
        blank=True,
        help_text='Enter the email addresses you want to carbon copy (CC). Separate multiple addresses with commas.'
    )
    email_bcc = models.TextField(
        null=True,
        blank=True,
        help_text='Enter the email addresses you want to blind carbon copy (BCC). Separate multiple addresses with commas.'
    )
    tracking_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    is_opened = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True)
    opened_at = models.DateTimeField(null=True,
                                     blank=True)

    def __str__(self):
        return self.email_to


class EmailTracking(models.Model):
    send_email = models.ForeignKey(
        SendEmail,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name='email_tracking',

    )
    ip_address = models.CharField(
        max_length=255,
        null=True,
        blank=False,
    )
    user_agent = models.CharField(
        max_length=500,  # Adjust the max length as needed
        null=True,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True)
    
    class Meta:
        verbose_name = "Mail Tracking"
        verbose_name_plural = "Mail Trackings"

    def __str__(self):
        return self.ip_address
