from leads.models import EmailTemplate,SendEmail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

import uuid

def generate_tracking_url():
    # Generate a unique tracking URL for the recipient
    tracking_id = str(uuid.uuid4())
    return tracking_id

def send_mail(id):
    try:
        obj = SendEmail.objects.get(id=id)
    except SendEmail.DoesNotExist:
        obj = None
    if obj is not None:
        email_to=obj.email_to
        send_to_name=obj.send_to_name
        email_cc=obj.email_cc
        if email_cc:
           email_cc = email_cc.split(',')
        email_bcc=obj.email_bcc
        if email_bcc:
           email_bcc = email_bcc.split(',')
        subject=obj.email_template.subject
        email_body=obj.email_template.email_body

        context = {}
        
        context['send_to_name'] = send_to_name
        email_body = email_body.replace("{NAME}", send_to_name)
        context['email_body'] = email_body
        tracking_id=generate_tracking_url()
        tracking_url=f"https://tropolite.com/track/{tracking_id}"
        context['tracking_url'] =tracking_url
        obj.tracking_id=tracking_id
        obj.save()
        message = render_to_string('emails/custom_mail.html', context)

        with get_connection(
        host="smtp.office365.com",
        port=587,
        username="info@tropolite.com",
        password="Kuk46136",
        use_tls=True
        ) as connection:
            email_from = "Tropolite Foods <info@tropolite.com>"
            recipient_list = [email_to,]
            to_bcc = email_bcc
            cc_recipients= email_cc
            subject = subject
           
            msg = EmailMessage(subject, message, email_from, recipient_list, cc=cc_recipients, bcc=to_bcc,connection=connection)
            msg.content_subtype = 'html'  # Set content type to HTML
            msg.send()

    return HttpResponse("Sent successfully!")




