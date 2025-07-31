from django.contrib import admin
from .models import CustomUser, Category, Article, Commentaire

# Register your models here.
# siteblog/admin.py


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'created_at', 'deleted_at')
    list_filter = ('is_admin', 'deleted_at')
    search_fields = ('username', 'email')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'deleted_at')
    list_filter = ('deleted_at',)
    search_fields = ('name',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'deleted_at')
    list_filter = ('category', 'deleted_at')
    search_fields = ('title', 'content')

class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'content', 'created_at', 'deleted_at')
    list_filter = ('article', 'deleted_at')
    search_fields = ('content',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Commentaire, CommentaireAdmin)