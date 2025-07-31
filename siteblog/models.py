# siteblog/models.py
from django.db import models
from django.contrib.auth.hashers import check_password,make_password
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        if not username:
            raise ValueError("Le nom d'utilisateur est requis")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = password  # Stockage en texte brut
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(BaseModel):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Champ déjà défini
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return self.password == raw_password

    def get_username(self):
        return self.username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return self.username
class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Article(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(upload_to='articles/photos/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Commentaire(BaseModel):
    content = models.TextField()
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='commentaires')
    author = models.ForeignKey('CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"Commentaire par {self.author or 'Anonyme'} sur {self.article}"