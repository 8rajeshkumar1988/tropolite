from django.urls import include, path
from .import views
urlpatterns = [
    path('about-us', views.about_us, name="about_us"),
    path('leadership', views.leadership, name="leadership"),
    path('dealer-locator', views.bakery_locator, name="bakery_locator"),
    path('food-dairy-technology', views.food_dairy_technology, name="food_dairy_technology"),
    path('contact-us', views.contact_us, name="contact_us"),
    path('our-journey', views.our_journey, name="our_journey"),
    path('our-brand', views.our_brand, name="our_brand"),
    path('our-customers', views.our_customers, name="our_customers"),
    path('manufacturing-capabilities', views.factory, name="factory"),
    path('career', views.jobs, name="career"),
    path('csr', views.csr, name="csr"),
    path('events-and-exhibitions', views.events, name="events-and-exhibitions"),
    path('event_list', views.event_list, name="event_list"),
    path('event_gallery', views.event_gallery, name="event_gallery"),
    path('patents-certificates', views.patents_certificates, name="patents_certificates"),
    path('microbial-biotechnology', views.microbial_biotechnology, name="microbial_biotechnology"),
    path('tropolite-prime', views.artisan, name="artisan"),
    path('job_apply', views.job_apply, name="job_apply"),
    path('csr-reports', views.csrreport, name="csrreport"),
    path('csrreportList', views.csrreportList, name="csrreportList"),
    path('bakery_listing', views.bakery_listing, name="bakery_listing"),
    path('save_lead', views.save_lead, name="save_lead"),
    path('all-products', views.all_products, name="all_products"),
    path('all-products/<slug:category>', views.all_products, name="all_products"),
    path('faqs', views.faq, name="faqs"),
    path('privacy-policy', views.privacy_policy, name="privacy_and_policy_page"),
    path('job-apply-email', views.job_appply_email, name="job_apply_email"),   
    path('send_lead', views.export_csv_and_send_email, name="send_lead"),   
    path('home-page', views.index2, name="home2"),  
    path('track/<slug:slug>', views.track, name="track"), 
]




