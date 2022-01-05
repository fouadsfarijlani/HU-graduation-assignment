from django import forms
from .models import ItemClassificationPicture, ItemClassificationResults
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



#class ImageClassificationForm(forms.Form):

 #   picture = forms.ImageField()


class ImageClassificationForm(forms.ModelForm):
    
   
    class Meta:
        model = ItemClassificationPicture
        fields = ('picture',)

       # widgets = {
       #     'picture' : forms.ImageField(attrs = {'class':'btn btn-outline-success'})
       # }
    #img_name = forms.CharField(max_length = 250)
   # img_field = forms.ImageField()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ImageClassificationRectifiedResults(forms.ModelForm):
    
    class Meta:
        model = ItemClassificationResults
        fields = ['rectified_label', 'marked_for_futur_training']