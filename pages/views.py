from django.core.files import File
import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from app.models import (
    Statics,
    CsrReport,
    CsrHighlight,
    Bakery,
    Category,
    Faq,
    CsrCategory,
)
from app.utils import (
    category_list,
    get_page_data,
    get_random_recipes,
    get_breadcrumb_json,
)
from products.models import Product
from jobs.models import Job, JobApply, JobDepartment
from leads.models import Lead, SendEmail, EmailTracking
from .forms import JobApplyForm, LeadForm
from events.models import Event, EventGallery
import json
import datetime
import requests

# from datetime import datetime

from geopy.geocoders import Nominatim

import re
import math
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from pages.forms import LeadForm

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from urllib.request import urlretrieve
import csv
from django.utils import timezone

from .models import (
    Leadership,
    LeadershipGroupImage,
    AboutUsImage,
    OurBrand,
    CarrerImage,
    CsrImage,
    PatentsCertificatesImage,
    FoodDairyTechnologyImage,
    MicrobialBiotechnologyImage,
)


def index2(request):
    context = {}
    context["page_name"] = "home2"
    context["category_list"] = category_list()
    context["load_vimeo_js"] = "N"

    page_info = get_page_data("home")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "home"
        context["heading"] = "home"
        context["meta_keywords"] = ""
        context["meta_description"] = ""

    statics = Statics.objects.all().order_by("sequence_number").filter(is_active=True)
    context["statics"] = statics
    context["page_url"] = request.build_absolute_uri()
    # customers_left = Customer.objects.all().order_by(
    #     "sequence_number").filter(is_active=True, direction='left')
    # context['customers_left'] = customers_left

    # customers_right = Customer.objects.all().order_by(
    #     "sequence_number").filter(is_active=True, direction='right')
    # context['customers_right'] = customers_right
    context["random_1_recipes"] = get_random_recipes(1)
    context["random_4_recipes"] = get_random_recipes(4)
    context["leadform"] = LeadForm()

    return render(request, "front/home2.html", context)


def validate_mobile_number(number):
    pattern = re.compile(r"^[6789]\d{9}$")
    if re.match(pattern, number):
        return True
    else:
        return False


def all_products(request, **kwargs):
    context = {}
    context["page_name"] = "all_products"
    context["category_list"] = category_list()
    breadcrumbs = []

    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)

    slug = kwargs.get("category")
    if slug:
        try:
            category_data = Category.objects.get(slug=slug, is_active=True)
            if category_data.meta_title:
                context["title"] = category_data.name
                context["meta_title"] = category_data.meta_title
            else:
                context["title"] = category_data.name
                context["meta_title"] = category_data.name

            bcrumbs = {}
            bcrumbs["heading"] = category_data.name
            bcrumbs["slug"] = "/" + category_data.slug
            breadcrumbs.insert(1, bcrumbs)
        except Category.DoesNotExist:
            category_data = None
    else:
        category_data = None

    page_info = get_page_data("all-products")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "All Products"
        context["meta_title"] = "All Products"
        context["heading"] = "All Products"
        context["meta_keywords"] = ""
        context["meta_description"] = ""

    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    if category_data is not None:
        breadcrumbs.insert(2, bcrumbs)
    else:
        breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs

    context["category_data"] = category_data

    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "all-products")
    )

    products = (
        Product.objects.all()
        .order_by("sequence_number")
        .filter(is_active=True)
        .order_by("?")
    )
    if category_data is not None:
        products = products.filter(category=category_data.id)
    context["products"] = products

    context["random_1_recipes"] = get_random_recipes(1)
    context["random_4_recipes"] = get_random_recipes(4)
    form_data = {}
    context["leadform"] = LeadForm(form_data)
    return render(request, "front/all_products.html", context)


def artisan(request):
    context = {}
    context["page_name"] = "subcategory"
    context["category_list"] = category_list()
    breadcrumbs = []

    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)

    page_info = get_page_data("tropolite-prime")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Artisan"
        context["meta_title"] = "Artisan"
        context["heading"] = "Artisan"
        context["meta_keywords"] = ""
        context["meta_description"] = ""

    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "tropolite-prime")
    )

    products = (
        Product.objects.all()
        .order_by("sequence_number")
        .filter(is_active=True, tags__slug="prime")
        .order_by("?")
    )
    context["products"] = products

    list_json = []
    if products:
        for index, blg in enumerate(products):
            ListArr = {}
            ListArr["@type"] = "Product"
            ListArr["name"] = blg.name
            ListArr["url"] = request.build_absolute_uri() + "/" + blg.slug
            ListArr["image"] = blg.image.url
            ListArr["description"] = blg.short_description
            ListArr["position"] = index
            brand = {"@type": "Brand", "name": "Tropolite"}
            ListArr["brand"] = brand
            aggregateRating = {
                "@type": "AggregateRating",
                "ratingValue": "5",
                "reviewCount": 10000,
            }
            ListArr["aggregateRating"] = aggregateRating
            list_json.insert(index, ListArr)

    context["list_json"] = json.dumps(list_json)

    context["random_1_recipes"] = get_random_recipes(1)
    context["random_4_recipes"] = get_random_recipes(4)
    context["leadform"] = LeadForm()
    return render(request, "front/artisan.html", context)


def about_us(request):
    context = {}
    context["page_name"] = "about_us"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("about-us")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "About us"
        context["heading"] = "About us"
        context["meta_title"] = "About us"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    statics = Statics.objects.all().order_by("sequence_number").filter(is_active=True)
    context["statics"] = statics

    try:
        about_us_images = AboutUsImage.objects.get(page_id=page_info["page_id"])
        about_us_images = about_us_images
    except AboutUsImage.DoesNotExist:
        about_us_images = None

    context["about_us_images"] = about_us_images

    ourbrands = (
        OurBrand.objects.all()
        .order_by("sequence_number")
        .filter(is_active=True, page_id=page_info["page_id"])
    )
    context["ourbrands"] = ourbrands

    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "about-us")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/about_us.html", context)


def leadership(request):
    context = {}
    context["page_name"] = "leadership"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("leadership")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Leadership"
        context["meta_title"] = "Leadership"
        context["heading"] = "Leadership"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "leadership")
    )
    context["leadform"] = LeadForm()

    try:
        leadershipimage = LeadershipGroupImage.objects.get(page_id=page_info["page_id"])
    except LeadershipGroupImage.DoesNotExist:
        leadershipimage = None

    context["leadershipimage"] = leadershipimage

    leaderships = (
        Leadership.objects.all()
        .order_by("sequence_number")
        .filter(is_active=True, page_id=page_info["page_id"])
    )
    context["leaderships"] = leaderships

    return render(request, "front/leadership.html", context)


def faq(request):
    context = {}
    context["page_name"] = "faqs"
    context["load_vimeo_js"] = "N"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("faqs")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "FAQS"
        context["heading"] = "FAQS"
        context["meta_title"] = "FAQS"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "faqs")
    )

    faq_list = Faq.objects.all().order_by("sequence_number").filter(is_active=True)
    context["faq_list"] = faq_list
    list_json = []
    faqs = [
        {
            "@type": "Question",
            "name": faq.question,
            "acceptedAnswer": {"@type": "Answer", "text": faq.answer},
        }
        for faq in faq_list
    ]

    list_json = json.dumps(faqs, indent=2)
    context["list_json"] = list_json
    context["leadform"] = LeadForm()

    return render(request, "front/faqs.html", context)


def privacy_policy(request):
    context = {}
    context["page_name"] = "Privacy Policy "
    context["load_vimeo_js"] = "N"
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("privacy-policy")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Privacy Policy"
        context["heading"] = "Privacy Policy"
        context["meta_title"] = "Privacy Policy"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "privacy-policy")
    )
    context["leadform"] = LeadForm()
    context["category_list"] = category_list()
    return render(request, "front/privacy_policy.html", context)


def bakery_locator(request):
    context = {}
    context["page_name"] = "bakery_locator"
    context["load_vimeo_js"] = "N"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("dealer-locator")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Bakery locator"
        context["heading"] = "Bakery locator"
        context["meta_title"] = "Bakery locator"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "dealer-locator")
    )

    pincodes = (
        Bakery.objects.all()
        .order_by("name")
        .filter(is_active=True)
        .values_list("pin_code", flat=True)
        .distinct()
    )
    context["pincodes"] = pincodes
    context["pin_code"] = request.GET.get("pin_code")

    # context['locations'] = location_list(request)
    context["leadform"] = LeadForm()
    return render(request, "front/bakery_locator.html", context)


def csrreport_list(request):
    context = {}
    year = request.GET.get("year")
    csrreports = CsrReport.objects.all().order_by("-report_date").filter(is_active=True)

    if year is not None and year:
        csrreports = csrreports.filter(report_date__year=year)

    context["csrreports"] = csrreports
    return render(request, "front/csr_report_list.html", context)


def csrreportList(request):
    context = {}
    year = request.GET.get("year")
    csrcategory = request.GET.get("csrcategory")
    csrreports = CsrReport.objects.all().order_by("-report_date").filter(is_active=True)

    if year is not None and year:
        csrreports = csrreports.filter(report_date__year=year)
    if csrcategory is not None and csrcategory:
        csrreports = csrreports.filter(csr_category_id=csrcategory)
    context["csrreports"] = csrreports

    return render(request, "front/csr_report_list.html", context)


def get_state_name(pin_code):
    url = "https://api.postalpincode.in/pincode/" + str(pin_code)
    payload = {}
    headers = {}
    State = ""
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        json_data = response.json()
        if json_data:
            status_value = json_data[0]["Status"]
            if status_value == "Success":
                PostOffice = json_data[0]["PostOffice"]
                State = PostOffice[0]["State"]

    return State


def location_list(request):
    array = []
    pin_code = request.GET.get("pin_code")
    state = request.GET.get("state")
    queryset = Bakery.objects.all().order_by("name").filter(is_active=True)
    if pin_code is not None and pin_code and pin_code != "None" and pin_code != "ALL":
        queryset = queryset.filter(pin_code=pin_code)
        if not queryset.exists():
            state = get_state_name(pin_code)
            queryset = (
                Bakery.objects.all()
                .order_by("name")
                .filter(is_active=True, state__iexact=state)
            )

    if state is not None and state and state != "None" and state != "ALL":
        queryset = queryset.filter(state=state)

    for query in queryset:
        rec = {}
        rec["id"] = query.id
        rec["name"] = query.name
        rec["state"] = query.state
        rec["city"] = query.city
        rec["pin_code"] = query.pin_code
        rec["contact_no"] = query.contact_no
        rec["latitude"] = query.latitude
        rec["longitude"] = query.longitude
        rec["address"] = query.address
        rec["is_active"] = query.is_active

        # lat1 = float(query.latitude)
        # lon1 = float(query.longitude)
        # if request.COOKIES.get('latitude') and request.COOKIES.get('longitude'):
        #    lat2 = float(request.COOKIES.get('latitude'))
        #    lon2 = float(request.COOKIES.get('longitude'))
        # else:
        #     lat2=0
        #     lon2=0

        # if lat2 and lon2:
        #   distance = haversine(lat1, lon1, lat2, lon2)
        # else:
        #    distance=None

        # rec['distance'] = distance
        array.insert((query.id), rec)

    return array


def haversine(lat1, lon1, lat2, lon2):
    import math

    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = R * c
    return round(distance)


def get_lat_long(state_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(state_name + ", India")
    if location:
        return [location.latitude, location.longitude]
    else:
        return None


def bakery_listing(request):
    context = {}
    context["locations"] = location_list(request)
    state = request.GET.get("state")
    if state is not None and state and state != "None" and state != "ALL":
        geocodes = get_lat_long(state)
    else:
        geocodes = None
    context["geocodes"] = geocodes

    return render(request, "front/bakery_listing.html", context)


def food_dairy_technology(request):
    context = {}
    context["page_name"] = "bakery_locator"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("food-dairy-technology")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Food & dairy technology"
        context["heading"] = "Food & dairy technology"
        context["meta_title"] = "Food & dairy technology"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "food-dairy-technology")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/food_dairy_technology.html", context)


def contact_us(request):
    context = {}
    context["page_name"] = "contact_us"
    context["load_vimeo_js"] = "N"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("contact-us")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Contact us"
        context["heading"] = "Contact us"
        context["meta_title"] = "Contact us"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]

    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["leadform"] = LeadForm()

    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "contact-us")
    )
    return render(request, "front/contact_us.html", context)


def our_journey(request):
    context = {}
    context["page_name"] = "our_journey"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("our-journey")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Our journey"
        context["heading"] = "Our journey"
        context["meta_title"] = "Our journey"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "our-journey")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/our_journey.html", context)


def our_brand(request):
    context = {}
    context["page_name"] = "our_brand"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("our-brand")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Our Brand"
        context["heading"] = "Our Brand"
        context["meta_title"] = "Our Brand"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "our-brand")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/our_brand.html", context)


def our_customers(request):
    context = {}
    context["page_name"] = "our_customers"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("our-customers")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Our Customers"
        context["heading"] = "Our Customers"
        context["meta_title"] = "Our Customers"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "our-customers")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/our_customers.html", context)


def factory(request):
    context = {}
    context["page_name"] = "manufacturing-capabilities"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("manufacturing-capabilities")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Manufacturing Capabilities"
        context["heading"] = "Manufacturing Capabilities"
        context["meta_title"] = "Manufacturing Capabilities"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "manufacturing-capabilities")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/factory.html", context)


def jobs(request):
    context = {}
    context["page_name"] = "Career"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("career")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Career"
        context["heading"] = "Career"
        context["meta_title"] = "Career"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["jobform"] = JobApplyForm()

    # departments = Job.objects.all().order_by(
    #     "job_department__sequence_number").filter(is_active=True).values_list('job_department__name', flat=True).distinct()
    context["departments"] = department_list()

    # jobs = Job.objects.all().order_by(
    #     "-id").filter(is_active=True)
    # context['jobs'] = jobs
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "career")
    )
    context["leadform"] = LeadForm()

    try:
        carrerimage = CarrerImage.objects.get(page_id=page_info["page_id"])
    except CarrerImage.DoesNotExist:
        carrerimage = None

    context["carrerimage"] = carrerimage

    return render(request, "front/jobs.html", context)


def department_list():
    array = []
    queryset = (
        JobDepartment.objects.all().order_by("sequence_number").filter(is_active=True)
    )
    for query in queryset:
        rec = {}
        rec["id"] = query.id
        rec["name"] = query.name
        rec["job_list"] = department_job_list(query.id)
        array.insert((query.id), rec)

    return array


def department_job_list(department):
    array = []
    queryset = (
        Job.objects.all()
        .order_by("id")
        .filter(is_active=True, job_department_id=department)
    )
    if queryset:
        for query in queryset:
            rec = {}
            rec["id"] = query.id
            rec["heading"] = query.heading
            rec["location"] = query.location
            rec["job_scope"] = query.job_scope
            rec["qualifications"] = query.qualifications
            rec["desired_experience_skills"] = query.desired_experience_skills
            rec["key_Responsibilities"] = query.key_Responsibilities
            rec["CTC_band"] = query.CTC_band

            array.insert((query.id), rec)

    return array


def export_csv_and_send_email(request):
    from io import StringIO  # Import StringIO from io module

    twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)

    records = Lead.objects.filter(created_at__gte=twenty_four_hours_ago)
    total_records_count = records.count()

    # Create CSV file

    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(
        [
            "Name",
            "Mobile",
            "Email",
            "Query",
            "City",
            "Zip Code",
            "State",
            "Category",
            "Sub Category",
            "Product",
        ]
    )  # Replace with your actual field names

    for record in records:
        if record.product:
            product = record.product
        else:
            product = "General Enquiry"

        if record.category:
            category = record.category
        else:
            category = "N.A"

        if record.subcategory:
            subcategory = record.subcategory
        else:
            subcategory = "N.A"

        csv_writer.writerow(
            [
                record.name,
                record.mobile,
                record.email,
                record.description,
                record.city,
                record.zip_code,
                record.state,
                category,
                subcategory,
                product,
            ]
        )

    context = {}
    context["total_records_count"] = total_records_count
    message = render_to_string("emails/lead_data.html", context)
    # return HttpResponse("Exported and sent successfully!"+message)
    current_date_time = datetime.datetime.now()
    formatted_date = current_date_time.strftime("%b %d, %Y")

    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        use_ssl=settings.EMAIL_USE_SSL,
    ) as connection:
        email_from = "Tropolite Foods"
        recipient_list = [
            "crmlead@tropilite.com",
        ]
        to_bcc = ["biz@jaiparekh.com"]
        subject = "New Lead Alerts- " + str(formatted_date) + " | Tropolite"
        msg = EmailMessage(
            subject, message, email_from, recipient_list, to_bcc, connection=connection
        )
        file_name = "Leads on " + str(formatted_date) + ".csv"
        msg.attach(file_name, csv_data.getvalue(), "text/csv")
        msg.content_subtype = "html"

        msg.send()

    return HttpResponse("Exported and sent successfully!")


def save_lead(request):
    response_data = {}
    if request.method == "POST":

        data = request.POST.copy()
        mobile = request.POST["mobile"]
        name = request.POST["name"]
        email = request.POST["email"]
        zip_code = request.POST["zip_code"]
        city = request.POST["city"]
        description = request.POST["description"]
        page = request.POST["page"]
        if name == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        if mobile == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
        else:
            if validate_mobile_number(mobile):
                isvalid = True
            else:
                response_data["error"] = True
                response_data["message"] = (
                    "The mobile number " + str(mobile) + " is not valid."
                )
                response_data["class"] = "error"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )

        if email == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
        else:
            try:
                validate_email(email)
                # Email is valid
            except ValidationError as e:
                response_data["error"] = True
                response_data["message"] = "*Enter a valid email."
                response_data["class"] = "error"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )

        if zip_code == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        if city == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        if page == "pop":
            category_id = request.POST["category_id"]
            if category_id == "":
                response_data["error"] = True
                response_data["message"] = (
                    "*All fields are mandatory. Please fill the missing fields."
                )
                response_data["class"] = "error"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )

            sub_category_id = request.POST["sub_category_id"]
            if sub_category_id == "":
                response_data["error"] = True
                response_data["message"] = (
                    "*All fields are mandatory. Please fill the missing fields."
                )
                response_data["class"] = "error"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )

        if description:
            url_pattern = r"http(s)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
            if re.search(url_pattern, description):
                response_data["status"] = True
                response_data["class"] = "error"
                response_data["message"] = "*URLs are not allowed in query field"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )
            else:
                is_continue = 1

        # if description == "":
        #     response_data['error'] = True
        #     response_data['message'] = "*All fields are mandatory. Please fill the missing fields."
        #     response_data['class'] = "error"
        #     response_data['errors'] = ""
        #     return HttpResponse(json.dumps(response_data), content_type="application/json")

        if mobile:
            if validate_mobile_number(mobile):
                lead_form = LeadForm(data)
                if lead_form.is_valid():
                    led_count = Lead.objects.filter(
                        name=name, mobile=mobile, email=email, description=description
                    ).count()
                    if led_count > 0:
                        response_data["status"] = True
                        response_data["class"] = "error"
                        response_data["message"] = "*You have already sent lead."
                        response_data["errors"] = ""
                        return HttpResponse(
                            json.dumps(response_data), content_type="application/json"
                        )
                    product_id = request.POST["product_id"]
                    if "category_id" in request.POST:
                        category_id = request.POST["category_id"]
                    else:
                        category_id = None

                    if "sub_category_id" in request.POST:
                        sub_category_id = request.POST["sub_category_id"]
                    else:
                        sub_category_id = None

                    leadform = lead_form.save(commit=False)
                    leadform.save()
                    if product_id and category_id and sub_category_id:
                        leadform.product_id = product_id
                        leadform.category_id = category_id
                        leadform.subcategory_id = sub_category_id
                        leadform.save()

                    elif category_id and sub_category_id:
                        leadform.category_id = category_id
                        leadform.subcategory_id = sub_category_id
                        leadform.save()

                    response_data = {}
                    response_data["error"] = False
                    response_data["message"] = (
                        "Our customer support team will get back to you promptly."
                    )
                    response_data["errors"] = ""
                else:
                    response_data = {}
                    response_data["error"] = True
                    response_data["message"] = ""
                    response_data["errors"] = lead_form.errors
            else:
                response_data["error"] = True
                response_data["message"] = (
                    "The Phone number " + str(mobile) + " is not valid."
                )
                response_data["class"] = "error"
                response_data["errors"] = ""
        else:
            response_data["error"] = True
            response_data["message"] = "Phone field is mandatory"
            response_data["class"] = "error"
            response_data["errors"] = ""

    else:
        response_data["error"] = True
        response_data["message"] = "Declined"
        response_data["class"] = "error"
        response_data["errors"] = ""
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def is_valid_image(image):
    max_size = 1024 * 1024 * 5  # 5 MB limit
    if image.name.lower().endswith(".pdf"):
        return image.size <= max_size
    elif image.name.lower().endswith(".heic"):
        return image.size <= max_size
    elif image.name.lower().endswith(".doc"):
        return image.size <= max_size
    elif image.name.lower().endswith(".docx"):
        return image.size <= max_size
    return False


def job_apply(request):
    response_data = {}
    if request.method == "POST":
        mobile = request.POST["mobile"]
        name = request.POST["name"]
        email = request.POST["email"]
        if name == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
        work_experience = request.POST["work_experience"]
        if work_experience == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        if email == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
        else:
            try:
                validate_email(email)
                # Email is valid
            except ValidationError as e:
                response_data["error"] = True
                response_data["message"] = "*Enter a valid email."
                response_data["class"] = "error"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )

        if mobile == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
        else:
            if validate_mobile_number(mobile):
                isvalid = True
            else:
                response_data["error"] = True
                response_data["message"] = (
                    "The mobile number " + str(mobile) + " is not valid."
                )
                response_data["class"] = "error"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )

        qualification = request.POST["qualification"]
        if qualification == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        current_location = request.POST["current_location"]
        if current_location == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        preferred_location = request.POST["preferred_location"]
        if preferred_location == "":
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )

        resume = request.FILES.get("resume")
        if resume is None:
            response_data["error"] = True
            response_data["message"] = (
                "*All fields are mandatory. Please fill the missing fields."
            )
            response_data["class"] = "error"
            response_data["errors"] = ""
            return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
        else:
            if not is_valid_image(resume):
                response_data["error"] = True
                response_data["message"] = "Resume maximum size to upload is 5MB"
                response_data["class"] = "error"
                response_data["errors"] = ""
                return HttpResponse(
                    json.dumps(response_data), content_type="application/json"
                )

        data = request.POST.copy()
        job_instance = Job.objects.get(pk=request.POST["job_id"])
        data["job"] = job_instance
        job_form = JobApplyForm(data, request.FILES)
        if job_form.is_valid():
            jobform = job_form.save(commit=False)
            jobform.job_id = request.POST["job_id"]
            jobform.save()
            send_email(jobform)

            response_data = {}
            response_data["error"] = False
            response_data["message"] = "Job applied Successfully"
            response_data["errors"] = ""
        else:
            response_data = {}
            response_data["error"] = True
            response_data["message"] = ""
            response_data["errors"] = job_form.errors

    else:
        response_data["error"] = True
        response_data["message"] = "Declined"
        response_data["class"] = "error"
        response_data["errors"] = ""
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def send_email(applicant):
    context = {}
    context["applicant"] = applicant
    message = render_to_string("emails/job_application.html", context)

    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        use_ssl=settings.EMAIL_USE_SSL,
    ) as connection:
        email_from = "Tropilite Foods"
        recipient_list = settings.SEND_EMAIL_NOTI_TO
        to_bcc = []
        subject = (
            "New Application Received | "
            + str(applicant.job.heading)
            + " - "
            + str(applicant.job.job_department.name)
        )
        msg = EmailMessage(
            subject, message, email_from, recipient_list, to_bcc, connection=connection
        )
        if applicant.resume:
            if settings.SERVER_TYPE == "P":
                msg.attach_file("/var/www/tropolite/media/" + str(applicant.resume))
            else:
                msg.attach_file("media/" + str(applicant.resume))
        # msg.attach_file('media/resume/9d198c41-cce0-47d5-819a-d52a8ac624c8-Terms_and_Conditions.docx')
        # this is required because there is no plain text email version
        msg.content_subtype = "html"

        msg.send()


def csr(request):
    context = {}
    context["page_name"] = "csr"
    context["category_list"] = category_list()

    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("csr")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "CSR"
        context["heading"] = "CSR"
        context["meta_title"] = "CSR"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()

    csrhighlights = (
        CsrHighlight.objects.all()
        .order_by("sequence_number")
        .filter(is_active=True)[:20]
    )
    context["csrhighlights"] = csrhighlights

    csrreports = (
        CsrReport.objects.all().order_by("-report_date").filter(is_active=True)[:3]
    )
    context["csrreports"] = csrreports
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "csr")
    )
    context["leadform"] = LeadForm()

    csr_category_list = (
        CsrCategory.objects.all().order_by("sequence_number").filter(is_active=True)
    )
    context["csr_category_list"] = csr_category_list


    try:
        csrimage = CsrImage.objects.get(page_id=page_info["page_id"])
    except CsrImage.DoesNotExist:
        csrimage = None

    context["csrimage"] = csrimage

    return render(request, "front/csr.html", context)


def csrreport(request):
    context = {}
    context["page_name"] = "csrreport"
    context["category_list"] = category_list()
    img = request.GET.get("img")
    csrcategoryid = request.GET.get("csrcategoryid")
    context["csrcategoryid"] = csrcategoryid
    context["img"] = img
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)

    bcrumbs = {}
    bcrumbs["heading"] = "CSR"
    bcrumbs["slug"] = "/csr"
    breadcrumbs.insert(1, bcrumbs)

    page_info = get_page_data("csr-reports")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "CSR Reports"
        context["heading"] = "CSR Reports"
        context["meta_title"] = "CSR Reports"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(2, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()

    csrreports = CsrReport.objects.all().order_by("-report_date").filter(is_active=True)

    year = request.GET.get("year", None)

    if year is not None and year:
        csrreports = csrreports.filter(report_date__year=year)
        context["year"] = year
    else:
        context["year"] = ""

    context["csrreports"] = csrreports

    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "csrreport")
    )
    context["leadform"] = LeadForm()
    csr_category_list = (
        CsrCategory.objects.all().order_by("sequence_number").filter(is_active=True)
    )
    context["csr_category_list"] = csr_category_list
    return render(request, "front/csrreport.html", context)


def events(request):
    context = {}
    context["page_name"] = "events"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("events-and-exhibitions")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Events"
        context["heading"] = "Events"
        context["meta_title"] = "Events"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = "events & exhibitions"
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["leadform"] = LeadForm()
    return render(request, "front/events.html", context)


def event_list(request):
    context = {}
    eventType = request.GET.get("eventtype")
    eventLists = Event.objects.all().order_by("created_at").filter(is_active=True)

    if eventType is not None and eventType:
        eventLists = eventLists.filter(event_type=eventType)
    context["eventlists"] = eventLists

    return render(request, "front/event_list.html", context)


def event_gallery(request):
    itemListElement = []

    albums = EventGallery.objects.all()
    event_id = request.GET.get("event_id")
    print(event_id)
    if event_id:
        albums = albums.filter(event=event_id)

    for album in albums:
        # Assuming you want to include both images and video embed codes

        if album.video_embed_code:
            item = {
                "video_embed_code": album.video_embed_code,
                "url": album.image.url,
                "caption": album.image_title,  # Or whatever you want to use as caption
            }
            itemListElement.append(item)
        else:
            item = {"url": album.image.url, "caption": album.image_title}
            itemListElement.append(item)

    return JsonResponse(itemListElement, safe=False)


def patents_certificates(request):
    context = {}
    context["page_name"] = "patents_certificates"
    context["category_list"] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("patents-certificates")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Patents & Certificates"
        context["heading"] = "Patents & Certificates"
        context["meta_title"] = "Patents & Certificates"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "patents-certificates")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/patents_certificates.html", context)


def microbial_biotechnology(request):
    context = {}
    context["page_name"] = "microbial_biotechnology"
    context["category_list"] = category_list()

    breadcrumbs = []
    bcrumbs = {}
    bcrumbs["heading"] = "Tropolite"
    bcrumbs["slug"] = "/"
    breadcrumbs.insert(0, bcrumbs)
    page_info = get_page_data("microbial-biotechnology")
    if page_info:
        context.update(page_info)
    else:
        context["title"] = "Microbial biotechnology"
        context["heading"] = "Microbial biotechnology"
        context["meta_title"] = "Microbial biotechnology"
        context["meta_keywords"] = ""
        context["meta_description"] = ""
    bcrumbs = {}
    bcrumbs["heading"] = context["title"]
    bcrumbs["slug"] = ""
    breadcrumbs.insert(1, bcrumbs)
    context["breadcrumbs"] = breadcrumbs
    context["page_url"] = request.build_absolute_uri()
    context["itemListElement"] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "microbial-biotechnology")
    )
    context["leadform"] = LeadForm()
    return render(request, "front/microbial_biotechnology.html", context)


def job_appply_email(request):
    context = {}
    context["page_name"] = "jop apply email"
    context["title"] = "jop apply email"
    context["meta_title"] = "jop apply email"
    context["meta_keywords"] = ""
    context["meta_description"] = ""
    return render(request, "emails/job_application.html", context)


def get_client_ip(request):
    ipaddress = ""
    if "HTTP_CLIENT_IP" in request.META:
        ipaddress = request.META["HTTP_CLIENT_IP"]
    elif "HTTP_X_FORWARDED_FOR" in request.META:
        ipaddress = request.META["HTTP_X_FORWARDED_FOR"]
    elif "HTTP_X_FORWARDED" in request.META:
        ipaddress = request.META["HTTP_X_FORWARDED"]
    elif "HTTP_FORWARDED_FOR" in request.META:
        ipaddress = request.META["HTTP_FORWARDED_FOR"]
    elif "HTTP_FORWARDED" in request.META:
        ipaddress = request.META["HTTP_FORWARDED"]
    elif "REMOTE_ADDR" in request.META:
        ipaddress = request.META["REMOTE_ADDR"]
    else:
        ipaddress = "UNKNOWN"
    return ipaddress


def track(request, **kwargs):
    tracking_id = kwargs.get("slug")
    try:
        obj = SendEmail.objects.get(tracking_id=tracking_id)
    except SendEmail.DoesNotExist:
        obj = None
    if obj is not None:
        obj.is_opened = True
        obj.opened_at = datetime.datetime.now()
        obj.save()
        user_agent = request.META.get("HTTP_USER_AGENT")
        ip_address = get_client_ip(request)
        tracking = EmailTracking()
        tracking.send_email_id = obj.id
        tracking.ip_address = ip_address
        tracking.user_agent = user_agent
        tracking.save()

    return HttpResponse("Sent successfully!")
