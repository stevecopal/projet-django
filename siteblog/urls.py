# siteblog/urls.py
from django.urls import path
from . import views
from .views import (
    HomeView, RegisterView, LoginView, LogoutView, CreateArticleView,
    ArticleDetailView, DeleteArticleView ,ManageCategoriesView,CreateCategoryView,UpdateCategoryView,
    DeleteCategoryView, CommentCreateView ,CommentUpdateView ,CommentDeleteView
)
from .views import CreateUserView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('article/create/', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:article_id>/delete/', DeleteArticleView.as_view(), name='delete_article'),
    path('category/manage/', ManageCategoriesView.as_view(), name='manage_categories'),
    
    path('category/create/', CreateCategoryView.as_view(), name='create_category'),
    path('category/<int:pk>/update/', views.UpdateCategoryView.as_view(), name='update_category'),
    path('category/<int:pk>/delete/', DeleteCategoryView.as_view(), name='delete_confirm_category'),
    
    path('article/<int:article_id>/comment/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    
    path('article/<int:pk>/edit/', views.ArticleDetailView.as_view(), name='update_article'),
    path('article/<int:pk>/delete/', views.DeleteArticleView.as_view(), name='delete_article'),
    
    path('users/manage/', views.ManageUsersView.as_view(), name='manage_users'),
    path('users/create/', views.CreateUserView.as_view(), name='create_user'),
    path('users/<int:pk>/update/', views.UpdateUserView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete_user'),
    
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/<int:user_id>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
]