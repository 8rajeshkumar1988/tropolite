from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from app.utils import category_list, get_random_recipes,get_random_products,get_page_data,get_breadcrumb_json
from .models import Recipe, Process,ProductFlavourImage
import random
from app.models import Tag
import json
from pages.forms import LeadForm 

def recipedetail(request, **kwargs):
    context = {}
    context['page_name'] = "recipedetail"
    context['category_list'] = category_list()
    slug = kwargs.get('slug')

    breadcrumbs = []
    bcrumbs = {}
    bcrumbs['heading'] = "Tropolite"
    bcrumbs['slug'] = "/"
    breadcrumbs.insert(0, bcrumbs)

   
    bcrumbs = {}
    bcrumbs['heading'] = "Recipes"
    bcrumbs['slug'] = "/recipes"
    breadcrumbs.insert(1, bcrumbs)

    try:
        recipe_data = Recipe.objects.get(slug=slug, is_active=True)
        bcrumbs = {}
        heading=recipe_data.heading
        if recipe_data.sub_heading:
            heading=heading+" "+recipe_data.sub_heading
        bcrumbs['heading'] = heading
        bcrumbs['slug'] = ""
        breadcrumbs.insert(2, bcrumbs)

    except Recipe.DoesNotExist:            
            context['page_name'] = "recipes_list"
            tag = slug
            breadcrumbs = []
            bcrumbs = {}
            bcrumbs['heading'] = "Tropolite"
            bcrumbs['slug'] = "/"
            breadcrumbs.insert(0, bcrumbs)
            page_info = get_page_data("recipes")
            if page_info:
                context.update(page_info)
            else:
                context['title'] = "Recipes"
                context['heading'] = "Recipes"
                context['meta_keywords'] = ""
                context['meta_description'] = ""

            

            recipes = Recipe.objects.all().order_by("-id").filter(is_active=True)
        
            
            
            if tag:
                try:
                    tag_data = Tag.objects.get(slug=tag, is_active=True)
                    bcrumbs = {}
                    bcrumbs['heading'] = context['title']
                    bcrumbs['slug'] = "/recipes"
                    breadcrumbs.insert(1, bcrumbs)
                    bcrumbs = {}
                    bcrumbs['heading'] = tag_data.name
                    bcrumbs['slug'] = ""
                    breadcrumbs.insert(2, bcrumbs)

                    context['title'] = str(tag_data.name)+" Delights | View Tropolite's Irresistible Recipes"
                    context['meta_title'] = str(tag_data.name)+" Delights | View Tropolite's Irresistible Recipes"
                    context['heading'] = str(tag_data.name)+" Delights | View Tropolite's Irresistible Recipes"
                    context['meta_keywords'] = ""
                    context['meta_description'] = "Indulge in "+str(tag_data.name)+" delights with Tropolite's irresistible recipes. Elevate your desserts & dishes. Explore our Bakery Academy & Recipe Books for delicious tips."

                except Tag.DoesNotExist:
                    bcrumbs = {}
                    bcrumbs['heading'] = context['title']
                    bcrumbs['slug'] = ""
                    breadcrumbs.insert(1, bcrumbs)
                recipes=recipes.filter(tags__slug=tag)
            else:
                bcrumbs = {}
                bcrumbs['heading'] = context['title']
                bcrumbs['slug'] = ""
                breadcrumbs.insert(1, bcrumbs)


            blog_list_json=[]
            if recipes:
                for index, blg in enumerate(recipes):
                    BlogArr = {}
                    BlogArr["@type"] = "Recipe"
                    heading=blg.heading
                    if blg.sub_heading:
                        heading=heading+" "+blg.sub_heading
                    BlogArr["name"] = heading
                    BlogArr["url"] = request.build_absolute_uri()+"/"+blg.slug
                    BlogArr["image"] = "https://tropolite.com/media/"+str(blg.image)
                    BlogArr["description"] = blg.description
                    BlogArr["position"] = index
                    # author = {
                    #     "@type": "Recipe",
                    #     "name": "Tropilite Foods Pvt. Ltd."
                    # }
                    # BlogArr["author"] = author
                    blog_list_json.insert(index, BlogArr)
            
            

            context['recipe_list_json'] = json.dumps(blog_list_json)    

            context['breadcrumbs'] = breadcrumbs
            context['recipes'] = recipes
            context['random_products'] = get_random_products()
            context['page_url'] = "https://tropolite.com/recipes/"+str(tag)
            context['itemListElement'] = json.dumps(get_breadcrumb_json(breadcrumbs,request,"recipes"))

            form_data = {
            }
            context['leadform'] = LeadForm(form_data)
            

            return render(request, 'front/recipes_list.html', context)

    if recipe_data.meta_title:
        context['title'] = recipe_data.meta_title
        context['meta_title'] = heading
    else:
        context['title'] = heading
        context['meta_title'] = heading
    
    if recipe_data.meta_image:
        context['meta_image'] = recipe_data.meta_image
    elif recipe_data.banner_image:
        context['meta_image'] = recipe_data.banner_image
    else:
        context['meta_image'] = recipe_data.image   
    
    # if  recipe_data.canonical_url:
    #     context['page_url'] = recipe_data.canonical_url   
    # else:
    context['page_url'] = request.build_absolute_uri()
    context['heading'] = heading
    context['meta_keywords'] = recipe_data.meta_keywords
    context['meta_description'] = recipe_data.meta_description
    context['recipe_data'] = recipe_data
    recipe_process_list = Process.objects.all().order_by(
        "sequence_number").filter(recipe=recipe_data.id)
    context['recipe_process_list'] = recipe_process_list

    recipe_flavour_list = ProductFlavourImage.objects.all().filter(recipe=recipe_data.id)
    context['recipe_flavour_list'] = {}
    

    context['random_1_recipes'] = get_random_recipes(1)
    context['random_4_recipes'] = get_random_recipes(4)
    context['breadcrumbs'] = breadcrumbs
    random_products = recipe_data.products.all() #get_random_products()
    randomitemList = []
    if random_products:
        for index, random_product in enumerate(random_products):
            fl_image=get_fl_image(random_product.id,recipe_data.id)
            if fl_image:
               random_product.image = fl_image
               randomitemList.insert(index, random_product)  
            else:    
                randomitemList.insert(index, random_product)

    context['random_products']=randomitemList
    context['itemListElement'] = json.dumps(get_breadcrumb_json(breadcrumbs,request,"recipes/"+slug))

    form_data = {
    }
    context['leadform'] = LeadForm(form_data)

    return render(request, 'front/recipedetail.html', context)

def get_fl_image(product_id,recipe_id):
    try:
       fls=ProductFlavourImage.objects.get(recipe_id=recipe_id,product_id=product_id)
       return fls.image
    except ProductFlavourImage.DoesNotExist:
        return False

def recipes_list(request):
    context = {}
    context['page_name'] = "recipes_list"
    context['category_list'] = category_list()

    tag = request.GET.get('tag')

    breadcrumbs = []
    bcrumbs = {}
    bcrumbs['heading'] = "Tropolite"
    bcrumbs['slug'] = "/"
    breadcrumbs.insert(0, bcrumbs)

    
    page_info = get_page_data("recipes")
    if page_info:
        context.update(page_info)
    else:
        context['title'] = "Recipes"
        context['heading'] = "Recipes"
        context['meta_keywords'] = ""
        context['meta_description'] = ""

    

    recipes = Recipe.objects.all().order_by("-id").filter(is_active=True)
   
      
    
    if tag:
        try:
            tag_data = Tag.objects.get(slug=tag, is_active=True)
            bcrumbs = {}
            bcrumbs['heading'] = context['title']
            bcrumbs['slug'] = "recipes"
            breadcrumbs.insert(1, bcrumbs)
            bcrumbs = {}
            bcrumbs['heading'] = tag_data.name
            bcrumbs['slug'] = ""
            breadcrumbs.insert(2, bcrumbs)

            context['title'] = str(tag_data.name)+" Delights | View Tropolite's Irresistible Recipes"
            context['meta_title'] = str(tag_data.name)+" Delights | View Tropolite's Irresistible Recipes"
            context['heading'] = str(tag_data.name)+" Delights | View Tropolite's Irresistible Recipes"
            context['meta_keywords'] = ""
            context['meta_description'] = "Indulge in "+str(tag_data.name)+" delights with Tropolite's irresistible recipes. Elevate your desserts & dishes. Explore our Bakery Academy & Recipe Books for delicious tips."

        except Tag.DoesNotExist:
            bcrumbs = {}
            bcrumbs['heading'] = context['title']
            bcrumbs['slug'] = ""
            breadcrumbs.insert(1, bcrumbs)
        recipes=recipes.filter(tags__slug=tag)
    else:
        bcrumbs = {}
        bcrumbs['heading'] = context['title']
        bcrumbs['slug'] = ""
        breadcrumbs.insert(1, bcrumbs)


    blog_list_json=[]
    if recipes:
        for index, blg in enumerate(recipes):
            BlogArr = {}
            BlogArr["@type"] = "Recipe"
            heading=blg.heading
            if blg.sub_heading:
                heading=heading+" "+blg.sub_heading
            BlogArr["name"] = heading
            BlogArr["url"] = request.build_absolute_uri()+"/"+blg.slug
            BlogArr["image"] = "https://tropolite.com/media/"+str(blg.image)
            BlogArr["description"] = blg.description
            BlogArr["position"] = index
            # author = {
            #     "@type": "Recipe",
            #     "name": "Tropilite Foods Pvt. Ltd."
            # }
            # BlogArr["author"] = author
            blog_list_json.insert(index, BlogArr)
    
    

    context['recipe_list_json'] = json.dumps(blog_list_json)    

    context['breadcrumbs'] = breadcrumbs
    context['recipes'] = recipes
    context['random_products'] = get_random_products()
    context['page_url'] = "https://tropolite.com/recipes"
    context['itemListElement'] = json.dumps(get_breadcrumb_json(breadcrumbs,request,"recipes"))

    form_data = {
    }
    context['leadform'] = LeadForm(form_data)
    

    return render(request, 'front/recipes_list.html', context)
