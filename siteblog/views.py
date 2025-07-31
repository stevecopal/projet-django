
from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404 , render
from django.urls import reverse_lazy
from .forms import RegistrationForm, LoginForm, ArticleForm
from .models import Article, CustomUser ,Category ,Commentaire
from .auth_backends import CustomAuthBackend
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import CategoryForm , CommentForm ,UserForm
from django.contrib import messages
from django import forms
from .forms import LoginForm,  PasswordResetRequestForm, PasswordResetConfirmForm


class HomeView(ListView):
    model = Article
    template_name = 'siteblog/home.html'
    context_object_name = 'articles'

    def get(self, request, *args, **kwargs):
        print(f"Utilisateur connecté : {request.user}, Authentifié : {request.user.is_authenticated}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Article.objects.filter(deleted_at__isnull=True)
    


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'}), label="Confirmer le mot de passe")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
    
class RegisterView(View):
    template_name = 'siteblog/register.html'
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                if CustomUser.objects.filter(username=username, deleted_at__isnull=True).exists():
                    messages.error(request, "Vérifiez vos informations : ce nom d'utilisateur est déjà pris.")
                elif CustomUser.objects.filter(email=email, deleted_at__isnull=True).exists():
                    messages.error(request, "Vérifiez vos informations : cet email est déjà utilisé.")
                else:
                    user = CustomUser.objects.create_user(username=username, email=email, password=password)
                    login(request, user)
                    messages.success(request, "Inscription réussie.")
                    return redirect('home')
            except Exception as e:
                messages.error(request, f"Vérifiez vos informations : {str(e)}")
        return render(request, self.template_name, {'form': form})
    

class LoginView(View):
    template_name = 'siteblog/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.get(username=username, deleted_at__isnull=True)
                if user.password == password and user.is_active:
                    login(request, user)
                    messages.success(request, "Connecté avec succès.")
                    return redirect('home')
                else:
                    messages.error(request, "Vérifiez vos informations.")
            except CustomUser.DoesNotExist:
                messages.error(request, "Vérifiez vos informations.")
        return render(request, self.template_name, {'form': form})
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'}))

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class CreateArticleView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'siteblog/article_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        print(f"Article créé : {article.title}")  # Pour déboguer
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"Erreurs du formulaire : {form.errors}")  # Pour déboguer
        return super().form_invalid(form)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'siteblog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, pk=self.kwargs['pk'], deleted_at__isnull=True)
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['commentaires'] = self.object.commentaires.filter(deleted_at__isnull=True)
        print("Contexte envoyé au template :", context.keys())  # Débogage
        return context
    
    
class DeleteArticleView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id, author=request.user, deleted_at__isnull=True)
        article.soft_delete()
        return redirect('home')
    
# siteblog/views.py
from django.contrib.auth.decorators import login_required

class ManageCategoriesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = 'siteblog/category_manage.html'
    context_object_name = 'categories'

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        return redirect('home')

    def get_queryset(self):
        return Category.objects.filter(deleted_at__isnull=True)
    

class CreateCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'siteblog/category_create.html'
    success_url = reverse_lazy('manage_categories')

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        return redirect('home')

class UpdateCategoryView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'siteblog/category_update.html'
    success_url = reverse_lazy('manage_categories')

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à modifier cette catégorie.")
        return redirect('home')

    def form_valid(self, form):
        messages.success(self.request, "Catégorie modifiée avec succès.")
        return super().form_valid(form)
    

class DeleteCategoryView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'siteblog/category_confirm_delete.html'
    success_url = reverse_lazy('manage_categories')

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à supprimer cette catégorie.")
        return redirect('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, "Catégorie supprimée avec succès.")
        return redirect(self.success_url)
    

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'siteblog/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['commentaires'] = self.object.commentaires.filter(deleted_at__isnull=True)
        return context

class CommentCreateView(CreateView):
    model = Commentaire
    form_class = CommentForm
    template_name = 'siteblog/comment_create.html'

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['article_id'], deleted_at__isnull=True)
        form.instance.article = article
        form.instance.author = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, "Commentaire ajouté avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.kwargs['article_id']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Commentaire
    form_class = CommentForm
    template_name = 'siteblog/comment_update.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à modifier ce commentaire.")
        return redirect('article_detail', pk=self.get_object().article.id)

    def form_valid(self, form):
        messages.success(self.request, "Commentaire modifié avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.get_object().article.id})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Commentaire
    template_name = 'siteblog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à supprimer ce commentaire.")
        return redirect('article_detail', pk=self.get_object().article.id)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, "Commentaire supprimé avec succès.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.article.id})
    


class ManageUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'siteblog/user_manage.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à gérer les utilisateurs.")
        return redirect('home')

    def get_queryset(self):
        return CustomUser.objects.filter(deleted_at__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = CustomUser.objects.filter(is_active=True, deleted_at__isnull=True).count()
        print("Contexte envoyé au template (ManageUsersView) :", context.keys())  # Débogage
        return context

class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'siteblog/user_create.html'
    success_url = reverse_lazy('manage_users')

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à créer un utilisateur.")
        return redirect('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data['password']:
            user.password = form.cleaned_data['password']  # Stockage en texte brut
        user.save()
        messages.success(self.request, f"Utilisateur {user.username} créé avec succès.")
        return super().form_valid(form)

class UpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'siteblog/user_update.html'
    success_url = reverse_lazy('manage_users')

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à modifier cet utilisateur.")
        return redirect('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data['password']:
            user.password = form.cleaned_data['password']  # Mise à jour du mot de passe
        user.save()
        messages.success(self.request, f"Utilisateur {user.username} modifié avec succès.")
        return super().form_valid(form)

class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'siteblog/user_confirm_delete.html'
    success_url = reverse_lazy('manage_users')

    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'êtes pas autorisé à supprimer cet utilisateur.")
        return redirect('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, f"Utilisateur {self.object.username} supprimé avec succès.")
        return redirect(self.success_url)
    

class PasswordResetRequestView(View):
    template_name = 'siteblog/password_reset_request.html'
    form_class = PasswordResetRequestForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email, deleted_at__isnull=True)
                return redirect('password_reset_confirm', user_id=user.id)
            except CustomUser.DoesNotExist:
                messages.error(request, "Aucun utilisateur associé à cet email.")
        return render(request, self.template_name, {'form': form})

class PasswordResetConfirmView(View):
    template_name = 'siteblog/password_reset_confirm.html'
    form_class = PasswordResetConfirmForm

    def get(self, request, user_id):
        form = self.form_class()
        user = get_object_or_404(CustomUser, id=user_id, deleted_at__isnull=True)
        return render(request, self.template_name, {'form': form, 'user_id': user_id})

    def post(self, request, user_id):
        form = self.form_class(request.POST)
        user = get_object_or_404(CustomUser, id=user_id, deleted_at__isnull=True)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                user.password = new_password
                user.save()
                messages.success(request, "Mot de passe réinitialisé avec succès. Vous pouvez maintenant vous connecter.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Erreur lors de la réinitialisation : {str(e)}")
        return render(request, self.template_name, {'form': form, 'user_id': user_id})