from django.shortcuts import render
from pages.models import Page
from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, SubCategory, TrustFactor, Statics, Customer, Type, SubType, Bakery
from products.models import Product, ProductAttributes, ProductColor, ProductGalery, ProductSize
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from app.utils import category_list, get_random_recipes, get_breadcrumb_json, get_page_data

import requests
from django.conf import settings
from pages.forms import LeadForm

from blogs.models import Blog
from recipes.models import Recipe
from leads.models import Campaign,CampaignTracking
from django.db.models import Q


def r1(request):
    # some code here
    return redirect('/bakery/whipping-creams', permanent=True)

def r2(request):
    # some code here
    return redirect('/bakery/whipping-creams/cook-n-whip-whipping-cream', permanent=True)

def r3(request):
    # some code here
    return redirect('/bakery/whipping-creams/wexford-whipping-cream', permanent=True)

def r4(request):
    # some code here
    return redirect('/bakery/whipping-creams/ecotrop-whipping-cream', permanent=True)

def r5(request):
    # some code here
    return redirect('/bakery/whipping-creams/neotrop-whipping-cream', permanent=True)

def r6(request):
    # some code here
    return redirect('/bakery/whipping-creams/premium-whipping-cream', permanent=True)

def r7(request):
    # some code here
    return redirect('/bakery/whipping-creams/svensons-whipping-cream', permanent=True)

def r8(request):
    # some code here
    return redirect('/bakery/whipping-creams/crystal-whipping-cream', permanent=True)

def redirect_to_home(request):
    # some code here
    return redirect('/', permanent=True)

def retocontact(request):
    # some code here
    return redirect('/contact-us', permanent=True)

def retonews(request, **kwargs):
    slug = kwargs.get('slug')
    try:
        blog_data = Blog.objects.get(Q(canonical_url=slug) | Q(slug=slug), is_active=True)
        return redirect('/blogs/'+str(blog_data.slug), permanent=True)
    except Blog.DoesNotExist:
        return redirect('/blogs', permanent=True)

def retorecipes(request, **kwargs):
    slug = kwargs.get('slug')
    try:
        recipe_data = Recipe.objects.get(canonical_url=slug, is_active=True)
        return redirect('/recipes/'+str(recipe_data.slug), permanent=True)
    except Recipe.DoesNotExist:
        return redirect('/recipes', permanent=True)    

def get_client_ip(request):
    ipaddress = ''
    if 'HTTP_CLIENT_IP' in request.META:
        ipaddress = request.META['HTTP_CLIENT_IP']
    elif 'HTTP_X_FORWARDED_FOR' in request.META:
        ipaddress = request.META['HTTP_X_FORWARDED_FOR']
    elif 'HTTP_X_FORWARDED' in request.META:
        ipaddress = request.META['HTTP_X_FORWARDED']
    elif 'HTTP_FORWARDED_FOR' in request.META:
        ipaddress = request.META['HTTP_FORWARDED_FOR']
    elif 'HTTP_FORWARDED' in request.META:
        ipaddress = request.META['HTTP_FORWARDED']
    elif 'REMOTE_ADDR' in request.META:
        ipaddress = request.META['REMOTE_ADDR']
    else:
        ipaddress = 'UNKNOWN'
    return ipaddress

def update_tracking(request):
    utm_source = request.GET.get('utm_source', '')  
    utm_campaign = request.GET.get('utm_campaign', '')
    utm_medium = request.GET.get('utm_medium', '')
    if utm_source and utm_campaign:
        if utm_medium:
            try:
               obj = Campaign.objects.get(utm_source=utm_source,utm_campaign=utm_campaign,utm_medium=utm_medium)
            except Campaign.DoesNotExist:
               obj = None
        else:
            try:
               obj = Campaign.objects.get(utm_source=utm_source,utm_campaign=utm_campaign)
            except Campaign.DoesNotExist:
               obj = None

        if obj is not None:
            user_agent = request.META.get('HTTP_USER_AGENT')
            ip_address = get_client_ip(request) 
            tracking=CampaignTracking()
            tracking.campaign_id=obj.id
            tracking.ip_address=ip_address
            tracking.user_agent=user_agent
            tracking.save()



def index(request):
    context = {}
    context['page_name'] = "home"
    context['category_list'] = category_list()

    page_info = get_page_data("home")
    if page_info:
        context.update(page_info)
    else:
        context['title'] = "Home"
        context['heading'] = "home"
        context['meta_keywords'] = ""
        context['meta_description'] = ""

    statics = Statics.objects.all().order_by(
        "sequence_number").filter(is_active=True)
    context['statics'] = statics
    context['page_url'] = request.build_absolute_uri()
    customers_left = Customer.objects.all().order_by(
        "sequence_number").filter(is_active=True, direction='left')
    context['customers_left'] = customers_left

    customers_right = Customer.objects.all().order_by(
        "sequence_number").filter(is_active=True, direction='right')
    context['customers_right'] = customers_right
    context['random_1_recipes'] = get_random_recipes(1)
    context['random_4_recipes'] = get_random_recipes(4)
    context['leadform'] = LeadForm()
    update_tracking(request)



    return render(request, 'front/home.html', context)

 



def sub_category_list(request):
    category_id = request.GET.get('category_id')
    category = SubCategory.objects.all().order_by('heading').filter(is_active=True)
    if category_id:
        category = SubCategory.objects.filter(
            category_id=category_id, is_active=True)
    data = {'list': list(category.values("id", "heading", "slug"))}
    respone = JsonResponse(data)
    return respone


def type_list(request):
    subcategory_id = request.GET.get('subcategory_id')
    types = Type.objects.all().order_by('name')
    if subcategory_id:
        types = Type.objects.order_by('name').filter(
            subcategory=subcategory_id)
    data = {'list': list(types.values("id", "name"))}
    respone = JsonResponse(data)
    return respone


def sub_type_list(request):
    type_id = request.GET.get('type_id')
    category = SubType.objects.all().order_by('name')
    if type_id:
        category = SubType.objects.order_by('name').filter(type=type_id)
    data = {'list': list(category.values("id", "name"))}
    respone = JsonResponse(data)
    return respone


def state_listing(request):
    response_data = {}
    options = []
    pin_code = request.GET.get('pin_code')
    if pin_code:
        bakerys = Bakery.objects.filter(is_active=True)
        bakerys = bakerys.filter(pin_code=pin_code)
        bakery = bakerys.first()
        if bakery:
            selectedstate = bakery.state
        else:
            selectedstate = None
    else:
        selectedstate = None
    queryset = Bakery.objects.all().order_by(
        "-state").filter(is_active=True).values_list('state', flat=True).distinct()
    counter = 0
    for state in queryset:
        rec = {}
        if selectedstate is None:
            isselected = False
        else:
            if (state == selectedstate):
                isselected = True
            else:
                isselected = False

        rec['id'] = state
        rec['name'] = state
        rec['selected'] = isselected
        options.insert((counter), rec)
        counter = counter+1
    response_data['error'] = False
    response_data['list'] = options
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def category(request, **kwargs):
    context = {}
    breadcrumbs = []
    slug = kwargs.get('slug')
    context['page_name'] = "category"
    context['category_list'] = category_list()
    bcrumbs = {}
    bcrumbs['heading'] = "Tropolite"
    bcrumbs['slug'] = "/"
    breadcrumbs.insert(0, bcrumbs)

    try:
        category_data = Category.objects.get(slug=slug, is_active=True)
    except Category.DoesNotExist:
        return redirect('/', permanent=True)
    if category_data.meta_title:
        context['title'] = category_data.name
        context['meta_title'] = category_data.meta_title
    else:
        context['title'] = category_data.name
        context['meta_title'] = category_data.name
    context['meta_image'] = category_data.meta_image
    context['category_data'] = category_data
    context['heading'] = context['title']
    bcrumbs = {}
    bcrumbs['heading'] = context['title']
    bcrumbs['slug'] = ""
    breadcrumbs.insert(1, bcrumbs)

    context['page_name'] = "category"

    subcategory_list = SubCategory.objects.all().order_by("sequence_number").filter(
        is_active=True, category=category_data.id)

    context['subcategory_list'] = subcategory_list

    list_json = []
    if subcategory_list:
        for index, blg in enumerate(subcategory_list):
            ListArr = {}
            ListArr["@type"] = "ListItem"
            ListArr["name"] = blg.heading
            ListArr["url"] = request.build_absolute_uri()+"/"+blg.slug
            ListArr["position"] = blg.sequence_number
            list_json.insert(index, ListArr)

    context['list_json'] = json.dumps(list_json)

    form_data = {
        'category_id': category_data.id,
    }
    context['leadform'] = LeadForm(form_data)

    context['meta_keywords'] = category_data.meta_keywords
    context['meta_description'] = category_data.meta_description
    context['breadcrumbs'] = breadcrumbs
    context['page_url'] = request.build_absolute_uri()
    context['random_1_recipes'] = get_random_recipes(1)
    context['random_4_recipes'] = get_random_recipes(4)
    context['itemListElement'] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, category_data.slug))

    products = Product.objects.all().order_by(
        "sequence_number").filter(is_active=True).order_by('?')
    if category_data is not None:
        products = products.filter(category=category_data.id)
    context['products'] = products
    update_tracking(request)

    return render(request, 'front/category.html', context)


def subcategory(request, **kwargs):
    context = {}
    context['page_name'] = "subcategory"
    context['category_list'] = category_list()
    context['load_vimeo_js'] = "N"
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs['heading'] = "Tropolite"
    bcrumbs['slug'] = "/"
    breadcrumbs.insert(0, bcrumbs)

    category = kwargs.get('category')

    try:
        category_data = Category.objects.get(slug=category, is_active=True)
        bcrumbs = {}
        bcrumbs['heading'] = category_data.name
        bcrumbs['slug'] = "/"+category_data.slug
        breadcrumbs.insert(1, bcrumbs)

    except Category.DoesNotExist:
        return redirect('/', permanent=True)

    subcategory = kwargs.get('subcategory')
    try:
        subcategory_data = SubCategory.objects.get(
            is_active=True, slug=subcategory, category=category_data.id)
        bcrumbs = {}
        bcrumbs['heading'] = subcategory_data.heading
        bcrumbs['slug'] = ""
        breadcrumbs.insert(2, bcrumbs)

    except SubCategory.DoesNotExist:
        return redirect('/', permanent=True)

    if subcategory_data.meta_title:
        context['title'] = subcategory_data.heading
        context['meta_title'] = subcategory_data.meta_title
    else:
        context['title'] = subcategory_data.heading
        context['meta_title'] = subcategory_data.heading
    context['meta_image'] = subcategory_data.meta_image
    context['heading'] = subcategory_data.heading
    context['meta_keywords'] = subcategory_data.meta_keywords
    context['meta_description'] = subcategory_data.meta_description

    context['breadcrumbs'] = breadcrumbs
    context['subcategory_data'] = subcategory_data

    form_data = {
        'category_id': category_data.id,
        'sub_category_id': subcategory_data.id
    }
    context['leadform'] = LeadForm(form_data)

    trust_facters = TrustFactor.objects.all().order_by(
        "sequence_number").filter(subcategory=subcategory_data.id)
    context['trust_facters'] = trust_facters

    products = Product.objects.all().order_by(
        "sequence_number").filter(subcategory=subcategory_data.id, is_active=True)
    context['products'] = products

    list_json = []
    if products:
        for index, blg in enumerate(products):
            ListArr = {}
            ListArr["@type"] = "Product"
            ListArr["name"] = blg.name
            ListArr["url"] = request.build_absolute_uri()+"/"+blg.slug
            ListArr["image"] = blg.image.url
            ListArr["description"] = blg.short_description
            ListArr["position"] = index
            brand = {
                "@type": "Brand",
                "name": "Tropolite"
            }
            ListArr["brand"] = brand
            aggregateRating = {
                "@type": "AggregateRating",
                "ratingValue": "5",
                "reviewCount": 10000
            }
            ListArr["aggregateRating"] = aggregateRating
            list_json.insert(index, ListArr)

    context['list_json'] = json.dumps(list_json)

    context['page_url'] = request.build_absolute_uri()
    context['random_1_recipes'] = get_random_recipes(1)
    context['random_4_recipes'] = get_random_recipes(4)
    context['product_list'] = get_product_list(subcategory_data.id)
    context['itemListElement'] = json.dumps(get_breadcrumb_json(
        breadcrumbs, request, category_data.slug+"/"+subcategory_data.slug))
    update_tracking(request)
    return render(request, 'front/subcategory.html', context)


def get_product_list(subcategory_id):
    array = []
    queryset = Type.objects.all().order_by(
        'sequence_number').filter(subcategory=subcategory_id)
    if not queryset.exists():
        rec = {}
        # rec['has_products'] = True
        # rec['name'] = ""
        # products = Product.objects.all().order_by(
        # "sequence_number").filter(subcategory=subcategory_id)
        # rec['products'] = products
        # array.insert((0), rec)
    else:
        for query in queryset:
            rec = {}
            rec['has_products'] = "0"
            rec['id'] = query.id
            rec['name'] = query.name
            rec['subtype_list'] = get_subtype(query.id, subcategory_id)
            array.insert((query.id), rec)

    return array


def get_subtype(type_id, subcategory_id):

    array = []
    queryset = SubType.objects.all().order_by(
        'sequence_number').filter(type=type_id)
    if not queryset.exists():
        rec = {}
        rec['has_products'] = 1
        rec['product_list'] = get_products_data(subcategory_id, type_id)
        array.insert((0), rec)
    else:
        for query in queryset:
            rec = {}
            rec['has_products'] = 0
            rec['id'] = query.id
            rec['name'] = query.name
            rec['product_list'] = get_products_data(
                subcategory_id, type_id, query.id)
            array.insert((query.id), rec)
    return array


def get_products_data(subcategory_id, type_id, sub_type_id=""):
    queryset2 = Product.objects.all().order_by(
        "sequence_number").filter(subcategory=subcategory_id, is_active=True, type=type_id)
    if sub_type_id:
        queryset2 = queryset2.filter(sub_type=sub_type_id)

    return queryset2


def productdetail(request, **kwargs):
    context = {}
    context['page_name'] = "productdetail"
    context['category_list'] = category_list()
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs['heading'] = "Tropolite"
    bcrumbs['slug'] = "/"
    breadcrumbs.insert(0, bcrumbs)

    category = kwargs.get('category')

    try:
        category_data = Category.objects.get(slug=category, is_active=True)
        bcrumbs = {}
        bcrumbs['heading'] = category_data.name
        bcrumbs['slug'] = "/"+category_data.slug
        breadcrumbs.insert(1, bcrumbs)

    except Category.DoesNotExist:
        return redirect('/', permanent=True)

    subcategory = kwargs.get('subcategory')
    try:
        subcategory_data = SubCategory.objects.get(
            is_active=True, slug=subcategory, category=category_data.id)
        bcrumbs = {}
        bcrumbs['heading'] = subcategory_data.heading
        bcrumbs['slug'] = "/"+category_data.slug+"/"+subcategory_data.slug
        breadcrumbs.insert(2, bcrumbs)

    except SubCategory.DoesNotExist:
        return redirect('/', permanent=True)

    productslug = kwargs.get('productslug')
    try:
        product_data = Product.objects.get(slug=productslug)
        bcrumbs = {}
        bcrumbs['heading'] = product_data.name
        bcrumbs['slug'] = ""
        breadcrumbs.insert(3, bcrumbs)

    except Product.DoesNotExist:
        return redirect('/', permanent=True)

    if product_data.meta_title:
        context['title'] = product_data.name
        context['meta_title'] = product_data.meta_title
    else:
        context['title'] = product_data.name
        context['meta_title'] = product_data.name

    if product_data.meta_image:
        context['meta_image'] = product_data.meta_image
    elif product_data.banner_image:
        context['meta_image'] = product_data.banner_image
    else:
        context['meta_image'] = product_data.image

    context['page_url'] = request.build_absolute_uri()
    form_data = {
        'product_id': product_data.id,
        'category_id': product_data.category_id,
        'sub_category_id': product_data.subcategory_id
    }
    context['leadform'] = LeadForm(form_data)
    context['heading'] = product_data.name
    context['meta_keywords'] = product_data.meta_keywords
    if product_data.meta_description:
        context['meta_description'] = product_data.meta_description
    else:
        context['meta_description'] = product_data.short_description
    context['short_description'] = product_data.short_description

    context['breadcrumbs'] = breadcrumbs
    context['product_data'] = product_data

    product_attributes = ProductAttributes.objects.all().order_by(
        "sequence_number").filter(product=product_data.id, is_active=True)
    context['product_attributes'] = product_attributes

    product_sizes = ProductSize.objects.all().order_by(
        "sequence_number").filter(product=product_data.id, is_active=True)
    context['product_sizes'] = product_sizes

    product_colors = ProductColor.objects.all().order_by(
        "sequence_number").filter(product=product_data.id, is_active=True)
    context['product_colors'] = product_colors

    product_galery = ProductGalery.objects.all().filter(
        product=product_data.id, is_active=True)
    context['product_galery'] = product_galery

    context['random_1_recipes'] = get_random_recipes(1)
    context['random_4_recipes'] = get_random_recipes(4)
    context['itemListElement'] = json.dumps(get_breadcrumb_json(
        breadcrumbs, request, category_data.slug+"/"+subcategory_data.slug+"/"+product_data.slug))
    update_tracking(request)

    return render(request, 'front/productdetail.html', context)






def InstagramPostsView(request):
    context={}
    access_token = settings.INSTAGRAM_ACCESS_TOKEN    
    user_info_url = f'https://graph.instagram.com/me?fields=id,username&access_token={access_token}'
    
    user_info_response = requests.get(user_info_url)
    if user_info_response.status_code != 200:
        return render(request, 'error.html', {'error': 'Failed to get user information'})
    
    user_info = user_info_response.json()
    print(user_info)
    user_id = user_info.get('id')    
    if not user_id:
        return render(request, 'error.html', {'error': 'User ID not found'})
        
    media_url = f'https://graph.instagram.com/{user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink&access_token={access_token}&limit=10'
    media_response = requests.get(media_url)
    if media_response.status_code != 200:
        return render(request, 'error.html', {'error': 'Failed to get media'})
    
    media_data = media_response.json()    
    context['posts'] =  media_data.get('data', [])    
    return render(request, 'front/include/instagram_posts.html', context)