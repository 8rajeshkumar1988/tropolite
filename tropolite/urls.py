"""
URL configuration for tropolite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from app import views
from django.views.generic import TemplateView

admin.site.site_header = 'ADMIN'
admin.site.site_title = "Tropilite Admin Portal"
admin.site.index_title = "Welcome to Tropilite Portal"
urlpatterns = [
    path('', views.index, name="index"),
    path('sub_category_list', views.sub_category_list),
    path('type_list', views.type_list),
    path('sub_type_list', views.sub_type_list),
    path('bakery/bakery-whips', views.r1, name="r1"),
    path('bakery/bakery-whips/cook-n-whip', views.r2, name="r2"),
    path('bakery/bakery-whips/wexford', views.r3, name="r3"),
    path('bakery/bakery-whips/ecotrop', views.r4, name="r4"),
    path('bakery/bakery-whips/neotrop', views.r5, name="r5"),
    path('bakery/bakery-whips/premium', views.r6, name="r6"),
    path('bakery/bakery-whips/svensons', views.r7, name="r7"),
    path('bakery/bakery-whips/crystal', views.r8, name="r8"),


    path('bakery/whipping-creams/cook-n-whip', views.r2, name="r2"),
    path('bakery/whipping-creams/wexford', views.r3, name="r3"),
    path('bakery/whipping-creams/ecotrop', views.r4, name="r4"),
    path('bakery/whipping-creams/neotrop', views.r5, name="r5"),
    path('bakery/whipping-creams/premium', views.r6, name="r6"),
    path('bakery/whipping-creams/svensons', views.r7, name="r7"),
    path('bakery/whipping-creams/crystal', views.r8, name="r8"),




    path('getInstaPost', views.InstagramPostsView, name="getInstaPost"),

    path('state_listing', views.state_listing, name="state_listing"),
    path('media/', views.redirect_to_home, name="redirect_to_home"),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    path('tropolite_sitemap.xml', TemplateView.as_view(template_name='tropolite_sitemap.xml', content_type='text/xml')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('admin/', admin.site.urls),
    path('pages/contact-us', views.retocontact, name="retocontact"),
    path('blogs/news/<slug:slug>', views.retonews, name="retonews"),
    path('blogs/recipes/<slug:slug>', views.retorecipes, name="retorecipes"),
    re_path(r'^blogs', include('blogs.urls')),
    re_path(r'^recipes', include('recipes.urls')),
    re_path('', include('pages.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('<slug:slug>', views.category, name="category"),
    path('<slug:category>/<slug:subcategory>', views.subcategory,name="subcategory"),
    path('<slug:category>/<slug:subcategory>/<slug:productslug>', views.productdetail,name="productdetail"),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
