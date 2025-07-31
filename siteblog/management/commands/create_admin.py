# siteblog/management/commands/create_admin.py
from django.core.management.base import BaseCommand
from siteblog.models import CustomUser

class Command(BaseCommand):
    help = 'Crée un utilisateur administrateur'

    def handle(self, *args, **kwargs):
        username = input("Nom d'utilisateur : ")
        email = input("Email : ")
        password = input("Mot de passe : ")
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=password,
            is_admin=True,
            is_active=True,
            is_staff=True  # Définit explicitement is_staff
        )
        self.stdout.write(self.style.SUCCESS(f"Administrateur {username} créé"))