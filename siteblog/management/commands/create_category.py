# siteblog/management/commands/create_category.py
from django.core.management.base import BaseCommand
from siteblog.models import Category

class Command(BaseCommand):
    help = 'Crée une catégorie'

    def handle(self, *args, **kwargs):
        name = input("Nom de la catégorie : ")
        description = input("Description (optionnel) : ")
        Category.objects.create(name=name, description=description)
        self.stdout.write(self.style.SUCCESS(f"Catégorie {name} créée"))