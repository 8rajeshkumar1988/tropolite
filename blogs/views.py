from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from app.utils import category_list, get_random_recipes, get_random_products, get_page_data, get_breadcrumb_json
from .models import Blog
from app.models import Tag
import json
import datetime
from pages.forms import LeadForm


def blog_list(request):
    context = {}
    context['page_name'] = "blog_list"
    context['category_list'] = category_list()
    tag = request.GET.get('tag')
    breadcrumbs = []
    bcrumbs = {}
    bcrumbs['heading'] = "Tropolite"
    bcrumbs['slug'] = "/"
    breadcrumbs.insert(0, bcrumbs)

    page_info = get_page_data("blogs")
    if page_info:
        context.update(page_info)
    else:
        context['title'] = "Blogs"
        context['heading'] = "Blogs"
        context['meta_keywords'] = ""
        context['meta_description'] = ""

    blogs = Blog.objects.all().order_by("-id").filter(is_active=True)
    if tag:
        try:
            tag_data = Tag.objects.get(slug=tag, is_active=True)
            bcrumbs = {}
            bcrumbs['heading'] = context['title']
            bcrumbs['slug'] = "blogs"
            breadcrumbs.insert(1, bcrumbs)
            bcrumbs = {}
            bcrumbs['heading'] = tag_data.name
            bcrumbs['slug'] = ""
            breadcrumbs.insert(2, bcrumbs)

        except Tag.DoesNotExist:
            bcrumbs = {}
            bcrumbs['heading'] = context['title']
            bcrumbs['slug'] = ""
            breadcrumbs.insert(1, bcrumbs)
        blogs = blogs.filter(tags__slug=tag)
    else:
        bcrumbs = {}
        bcrumbs['heading'] = context['title']
        bcrumbs['slug'] = ""
        breadcrumbs.insert(1, bcrumbs)
    blog_list_json = []
    if blogs:
        for index, blg in enumerate(blogs):
            BlogArr = {}
            BlogArr["@type"] = "BlogPosting"
            heading = blg.heading
            if blg.sub_heading:
                heading = heading+" "+blg.sub_heading
            BlogArr["headline"] = heading
            BlogArr["url"] = request.build_absolute_uri()+"/"+blg.slug
            BlogArr["image"] = "https://tropolite.com/media/"+str(blg.image)
            BlogArr["datePublished"] = blg.created_at.isoformat()
            BlogArr["description"] = blg.intro_description
            BlogArr["position"] = index
            BlogArr["author"] = {
                "@type": "Article",
                "name": "Tropilite Foods Pvt. Ltd."
            }
            blog_list_json.insert(index, BlogArr)

    context['blog_list_json'] = json.dumps(blog_list_json)
    context['breadcrumbs'] = breadcrumbs
    context['page_url'] = "https://tropolite.com/blogs"
    context['blogs'] = blogs
    context['random_products'] = get_random_products()
    context['itemListElement'] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "blogs"))
    form_data = {
    }
    context['leadform'] = LeadForm(form_data)
    return render(request, 'front/blog_list.html', context)


def blog_detail(request, **kwargs):
    context = {}
    context['page_name'] = "blog_detail"
    context['category_list'] = category_list()
    slug = kwargs.get('slug')

    breadcrumbs = []
    bcrumbs = {}
    bcrumbs['heading'] = "Tropolite"
    bcrumbs['slug'] = "/"
    breadcrumbs.insert(0, bcrumbs)

    bcrumbs = {}
    bcrumbs['heading'] = "Blogs"
    bcrumbs['slug'] = "/blogs"
    breadcrumbs.insert(1, bcrumbs)

    try:
        blog_data = Blog.objects.get(slug=slug)
        bcrumbs = {}
        heading = blog_data.heading
        if blog_data.sub_heading:
            heading = heading+" "+blog_data.sub_heading
        bcrumbs['heading'] = heading
        bcrumbs['slug'] = ""
        breadcrumbs.insert(2, bcrumbs)

    except Blog.DoesNotExist:
           
            context['page_name'] = "blog_list"
           
            tag = slug
            breadcrumbs = []
            bcrumbs = {}
            bcrumbs['heading'] = "Tropolite"
            bcrumbs['slug'] = "/"
            breadcrumbs.insert(0, bcrumbs)

            page_info = get_page_data("blogs")
            if page_info:
                context.update(page_info)
            else:
                context['title'] = "Blogs"
                context['heading'] = "Blogs"
                context['meta_keywords'] = ""
                context['meta_description'] = ""

            blogs = Blog.objects.all().order_by("-id").filter(is_active=True)
            if tag:
                try:
                    tag_data = Tag.objects.get(slug=tag, is_active=True)
                    bcrumbs = {}
                    bcrumbs['heading'] = context['title']
                    bcrumbs['slug'] = "/blogs"
                    breadcrumbs.insert(1, bcrumbs)
                    bcrumbs = {}
                    bcrumbs['heading'] = tag_data.name
                    bcrumbs['slug'] = ""
                    breadcrumbs.insert(2, bcrumbs)

                except Tag.DoesNotExist:
                    bcrumbs = {}
                    bcrumbs['heading'] = context['title']
                    bcrumbs['slug'] = ""
                    breadcrumbs.insert(1, bcrumbs)
                blogs = blogs.filter(tags__slug=tag)
            else:
                bcrumbs = {}
                bcrumbs['heading'] = context['title']
                bcrumbs['slug'] = ""
                breadcrumbs.insert(1, bcrumbs)
            blog_list_json = []
            if blogs:
                for index, blg in enumerate(blogs):
                    BlogArr = {}
                    BlogArr["@type"] = "BlogPosting"
                    heading = blg.heading
                    if blg.sub_heading:
                        heading = heading+" "+blg.sub_heading
                    BlogArr["headline"] = heading
                    BlogArr["url"] = request.build_absolute_uri()+"/"+blg.slug
                    BlogArr["image"] = "https://tropolite.com/media/"+str(blg.image)
                    BlogArr["datePublished"] = blg.created_at.isoformat()
                    BlogArr["description"] = blg.intro_description
                    BlogArr["position"] = index
                    BlogArr["author"] = {
                        "@type": "Article",
                        "name": "Tropilite Foods Pvt. Ltd."
                    }
                    blog_list_json.insert(index, BlogArr)

            context['blog_list_json'] = json.dumps(blog_list_json)
            context['breadcrumbs'] = breadcrumbs
            context['page_url'] = "https://tropolite.com/blogs/"+str(tag)
            context['blogs'] = blogs
            context['random_products'] = get_random_products()
            context['itemListElement'] = json.dumps(
                get_breadcrumb_json(breadcrumbs, request, "blogs"))
            form_data = {
            }
            context['leadform'] = LeadForm(form_data)
            return render(request, 'front/blog_list.html', context)

    if blog_data.meta_title:
        context['title'] = heading
        context['meta_title'] = blog_data.meta_title
    else:
        context['title'] = heading
        context['meta_title'] = heading

    if blog_data.meta_image:
        context['meta_image'] = blog_data.meta_image
    elif blog_data.banner_image:
        context['meta_image'] = blog_data.banner_image
    else:
        context['meta_image'] = blog_data.image

    # if blog_data.canonical_url:
    #     context['page_url'] = blog_data.canonical_url
    # else:
    context['page_url'] = request.build_absolute_uri()
    context['heading'] = heading
    context['meta_keywords'] = blog_data.meta_keywords
    if blog_data.meta_description:
        context['meta_description'] = blog_data.meta_description
    else:
        context['meta_description'] = blog_data.intro_description

    context['blog_data'] = blog_data
    context['breadcrumbs'] = breadcrumbs
    context['random_1_recipes'] = get_random_recipes(1)
    context['random_4_recipes'] = get_random_recipes(4)
    context['random_products'] = blog_data.products.all()
    context['itemListElement'] = json.dumps(
        get_breadcrumb_json(breadcrumbs, request, "blogs/"+slug))
    form_data = {
    }
    context['leadform'] = LeadForm(form_data)
    return render(request, 'front/blog_detail.html', context)
