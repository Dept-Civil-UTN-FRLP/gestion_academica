from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.usuarios.models import UserProfile


class Command(BaseCommand):
    help = "Crea un superusuario con perfil de superadmin"

    def handle(self, *args, **options):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        user = User.objects.create_superuser(username, email, password)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.es_superadmin = True
        profile.save()

        self.stdout.write(
            self.style.SUCCESS(f'Superadmin "{username}" creado exitosamente')
        )
