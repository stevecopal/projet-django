# siteblog/auth_backends.py
from .models import CustomUser

class CustomAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(username=username, deleted_at__isnull=True, is_active=True)
            if user.check_password(password):
                print(f"Utilisateur {username} authentifié avec succès")
                return user
            else:
                print(f"Échec de la vérification du mot de passe pour {username}")
                return None
        except CustomUser.DoesNotExist:
            print(f"Utilisateur {username} non trouvé ou non actif")
            return None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id, deleted_at__isnull=True, is_active=True)
            print(f"Utilisateur ID {user_id} récupéré avec succès")
            return user
        except CustomUser.DoesNotExist:
            print(f"Utilisateur ID {user_id} non trouvé ou non actif")
            return None