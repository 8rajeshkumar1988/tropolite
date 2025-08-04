from django import forms

from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from jobs.models import JobApply
from leads.models import Lead
from app.models import Category,SubCategory

class LeadForm(forms.ModelForm):
    product_id = forms.CharField(required=False, widget=forms.HiddenInput())
     
    category_id = forms.ModelChoiceField(required=False, 
        queryset=Category.objects.filter(is_active=True),empty_label="All Categories",widget=forms.Select(attrs={'class': 'input'})) 
    
    sub_category_id = forms.ModelChoiceField(required=False, 
        queryset=SubCategory.objects.filter(is_active=True),empty_label="All Sub Categories",widget=forms.Select(attrs={'class': 'input'}))


    name = forms.CharField(required=True, label='Name',max_length=50,widget=forms.TextInput(attrs={'onpaste':'return false;','ondrop':'return false;','autocomplete':'off','class': 'input alphaonly'}))
    email = forms.CharField(required=True, label='Email',max_length=100,widget=forms.TextInput(attrs={'autocomplete':'off','class': 'input','type': 'email'}))
    mobile = forms.CharField(required=True, label='Mobile',max_length=10,widget=forms.TextInput(attrs={'onpaste':'return false;','ondrop':'return false;','autocomplete':'off','class': 'input numbers','type': 'tel'}))
    zip_code = forms.CharField(required=True, label='Pincode',max_length=6,widget=forms.TextInput(attrs={'onpaste':'return false;','ondrop':'return false;','autocomplete':'off','class': 'input numbers zipcode'}))
    state = forms.CharField(required=True, label='State',widget=forms.TextInput(attrs={'onpaste':'return false;','ondrop':'return false;','autocomplete':'off','class': 'input id_state'}))
    city = forms.CharField(required=True, label='City',max_length=50,widget=forms.TextInput(attrs={'onpaste':'return false;','ondrop':'return false;','autocomplete':'off','class': 'input alphaonly'}))
    description = forms.CharField(required=False,widget=forms.Textarea(
        attrs={'name': 'description','autocomplete':'off','maxlength': 500,'onpaste':'return false;','ondrop':'return false;', 'rows': 5, 'cols': 30}))
    
   

    class Meta:
        model = Lead
        fields = ("category_id","sub_category_id","product_id","name", "email",'mobile','zip_code','state','city','description')

    # def __init__(self, *args, **kwargs):
    #     super(LeadForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'input'

class AllowedFileTypesValidator:
    def __init__(self, allowed_extensions=('PDF','pdf', 'doc', 'DOC', 'docx', 'DOCX')):
        self.allowed_extensions = allowed_extensions

    def __call__(self, value):
        if value:
            extension = value.name.split('.')[-1].lower()
            if extension not in self.allowed_extensions:
                raise ValidationError(
                    "Only PDF/DOC and DOCX files are allowed.")
            
class JobApplyForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name',max_length=50,widget=forms.TextInput(attrs={'class': 'inputjob alphaonly'}))
    work_experience = forms.CharField(required=True, label='Work experience', max_length=100,widget=forms.TextInput(attrs={'class': 'inputjob'}))
    email = forms.CharField(required=True, label='Email', max_length=100,widget=forms.TextInput(attrs={'type': 'email','class': 'inputjob'}))
    mobile = forms.CharField(required=True, label='Mobile',
                             max_length=10, widget=forms.TextInput(attrs={'class': 'inputjob numbers','type': 'tel'}))
    qualification = forms.CharField(required=True, label='Qualification',max_length=100,widget=forms.TextInput(attrs={'class': 'inputjob'}))
    current_location = forms.CharField(required=True, label='Current location',max_length=50,widget=forms.TextInput(attrs={'class': 'inputjob'}))
    preferred_location = forms.CharField(
        required=True, label='Preferred location',max_length=50,widget=forms.TextInput(attrs={'class': 'inputjob'}))
    resume = forms.FileField(
        required=True,
        label='resume',
        validators=[AllowedFileTypesValidator()],
    )
    
    job_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = JobApply
        fields = ("job_id", "name",'work_experience','email','mobile','qualification','current_location', "preferred_location", "resume")

    # def __init__(self, *args, **kwargs):
    #     super(JobApplyForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'inputjob'
