from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User as UserModel   
from PIL import Image, ImageOps








## USER LOGIN ETC ##



# class UserCreationFormulario(UserCreationForm):
#     email = forms.EmailField(label="Email", widget=forms.TextInput)
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

#     class Meta:
#         model = UserModel
#         fields = ["username", "password1", "password2", "email"]
#         help_texts = {k: "" for k in fields}

class UserCreationFormulario(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)


    class Meta:
        model = UserModel
        fields = ["username", "password1", "password2", "email"]
        help_texts = {k: "" for k in fields}




class UserEditionFormulario(UserChangeForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(label="Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)

    class Meta:
        model = UserModel
        fields = ["email", "first_name", "last_name"]
        help_texts = {k: "" for k in fields}


### BLOG ###
        
# class BlogPostForm(forms.ModelForm):
#     # Define the choices for the 'categoria' field
#     CATEGORIES_CHOICES = [
#         ('fitness', 'Fitness'),
#         ('nutrition', 'Nutrition'),
#         ('mental_health', 'Mental Health'),
#         ('wellness_tips', 'Wellness Tips'),
#         ('mindfulness', 'Mindfulness'),
#         ('recipes', 'Healthy Recipes'),
#         # Add more choices as needed
#     ]

#     categoria = forms.ChoiceField(choices=CATEGORIES_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

#     class Meta:
#         model = models.BlogPost
#         fields = ['titulo', 'contenido', 'categoria', 'post_image']

#     def clean_post_image(self):
#         post_image = self.cleaned_data.get('post_image')

#         if post_image:
#             img = Image.open(post_image)
#             max_size = (600, 600)  # Set your desired width and height

#             # Resize and maintain aspect ratio using ImageOps.fit
#             img = ImageOps.fit(img, max_size, Image.LANCZOS)
#             img = ImageOps.exif_transpose(img)

#             # Save the resized image back into the cleaned_data dictionary
#             output = BytesIO()
#             img.save(output, format='JPEG')
#             output.seek(0)
#             post_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % post_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

#         return post_image
        



class BlogPostForm(forms.ModelForm):
    # Define the choices for the 'categoria' field
    CATEGORIES_CHOICES = [
        ('fitness', 'Fitness'),
        ('nutrition', 'Nutrition'),
        ('mental_health', 'Mental Health'),
        ('wellness_tips', 'Wellness Tips'),
        ('mindfulness', 'Mindfulness'),
        ('recipes', 'Healthy Recipes'),
        # Add more choices as needed
    ]

    categoria = forms.ChoiceField(choices=CATEGORIES_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = models.BlogPost
        fields = ['titulo', 'contenido', 'categoria', 'post_image']

class UserAvatarFormulario(forms.ModelForm):

    class Meta:
        model = models.Avatar
        fields = ["imagen"]