from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {

            'meta_keywords': forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 4}),
            'name': forms.TextInput(attrs={'class': 'vLargeTextField'}),
            'slug': forms.TextInput(attrs={'class': 'vLargeTextField'}),
            'meta_title': forms.TextInput(attrs={'class': 'vLargeTextField'}),
        }
        fields = ['category', 'subcategory', 'type', 'sub_type', 'name', 'slug', 'sub_title', 'shelf_life', 'shelf_life_section_heading', 'shelf_life_section_subheading', 'shelf_life_section_temp_heading', 'storage_temp', 'background_color_code', 'short_description', 'description', 'used_directions', 'tags',
                'shop_now_url','meta_title', 'meta_keywords', 'meta_description', 'meta_image', 'image', 'is_tild_list_image', 'banner_image','video_embed_code' ,'video', 'is_active', 'sequence_number', 'heading_for_flavour_section']
