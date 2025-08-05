from app.models import Category, SubCategory
from pages.models import Page
from recipes.models import Recipe, Process
from django.db.models import Q
from products.models import Product


def get_base_url(request):
    is_secure = request.is_secure()
    scheme = 'https' if is_secure else 'http'
    base_url = f"{scheme}://{request.get_host()}"
    return base_url

def get_breadcrumb_json(bcrumbs,request,curent_slug):
    itemListElement = []
    for index, bcrumb in enumerate(bcrumbs):
        bscript = {}
        bscript["@type"] = "ListItem"
        bscript["position"] = index+1
        bscript["name"] = bcrumb['heading']
        if bcrumb['slug']:
           bscript["item"] = get_base_url(request)+str(bcrumb['slug'])
        else:
           bscript["item"] = get_base_url(request)+"/"+str(curent_slug)   
        itemListElement.insert(index, bscript)
    return itemListElement   

def get_random_products(category_id='', subcategory_id=''):
    products = Product.objects.filter(is_active=True)
    if category_id:
        products = products.filter(category=category_id)
    if category_id:
        products = products.filter(subcategory=subcategory_id)
    product_list = products.order_by('?')[:10]
    return product_list


def get_random_recipes(type='', category_id='', subcategory_id='', recipes_id=''):
    if type == 4:
        recipes = Recipe.objects.filter(is_active=True)
        if recipes_id:
            recipes = recipes.exclude(id=recipes_id)
        random_4_recipes = recipes.order_by('?')[:4]

        return random_4_recipes
    else:
        recipes = Recipe.objects.filter(is_active=True)
        recipes = recipes.filter(~Q(video__exact='') & ~Q(video__isnull=True))
        if recipes_id:
            recipes = recipes.exclude(id=recipes_id)
        random_1_recipes = recipes.order_by('?')[:1]
        if random_1_recipes.exists():
            return random_1_recipes
        else:
            recipes = Recipe.objects.filter(is_active=True)
            if recipes_id:
                recipes = recipes.exclude(id=recipes_id)
            random_1_recipes = recipes.order_by('?')[:1]
            return random_1_recipes


def get_page_data(page_slug):
    context = {}
    try:
        page_data = Page.objects.get(slug=page_slug, is_active=True)
        if page_data.meta_title:
            context['title'] = page_data.heading
            context['meta_title'] = page_data.meta_title
        else:
            context['title'] = page_data.heading
            context['meta_title'] = page_data.heading
        context['heading'] = page_data.heading
        context['page_id'] = page_data.id
        context['meta_image'] = page_data.meta_image
        context['meta_keywords'] = page_data.meta_keywords
        context['meta_description'] = page_data.meta_description
        context['page_schema'] = page_data.page_schema
    except Page.DoesNotExist:
        context = {}

    return context


def category_list():
    array = []
    queryset = Category.objects.all().order_by(
        'sequence_number').filter(is_active=True)
    for query in queryset:
        rec = {}
        rec['id'] = query.id
        rec['name'] = query.name
        rec['slug'] = query.slug
        rec['sequence'] = query.sequence_number
        rec['sub_category'] = parent_page_list(query.id)
        array.insert((query.id), rec)

    return array


def parent_page_list(category_id):
    array = []
    queryset = SubCategory.objects.all().order_by(
        'sequence_number').filter(is_active=True, category=category_id)
    for query in queryset:
        rec = {}
        rec['id'] = query.id
        rec['name'] = query.heading
        rec['slug'] = query.slug
        rec['sequence'] = query.sequence_number
        array.insert((query.id), rec)

    return array
