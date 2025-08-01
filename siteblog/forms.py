# siteblog/forms.py
from django import forms
from .models import CustomUser, Article, Category , Commentaire

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username, deleted_at__isnull=True).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email, deleted_at__isnull=True).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border rounded'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'photo': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['content' ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4}),
        }
        
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'}), required=False)
    is_admin = forms.BooleanField(required=False, label="Administrateur")
    is_active = forms.BooleanField(required=False, label="Actif")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_admin', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
        }
        

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}))

class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'}), label="Nouveau mot de passe")
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'}), label="Confirmer le nouveau mot de passe")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
    