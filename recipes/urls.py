from django.urls import include, path
from .import views
urlpatterns = [
   path('', views.recipes_list,name="recipes_list"),
   path('/<slug:slug>', views.recipedetail, name="recipedetail"),
]
