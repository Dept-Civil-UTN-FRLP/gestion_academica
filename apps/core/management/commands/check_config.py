from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config


class Command(BaseCommand):
    help = "Verifica la configuración de variables de entorno"

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("Verificando configuración..."))

        checks = {
            "SECRET_KEY": settings.SECRET_KEY
            != "django-insecure-default-key-change-this",
            "DEBUG": settings.DEBUG,
            "DATABASE": settings.DATABASES["default"]["NAME"] != "",
            "DB_PASSWORD": settings.DATABASES["default"]["PASSWORD"] != "",
            "EMAIL_HOST_USER": settings.EMAIL_HOST_USER != "",
            "ALLOWED_HOSTS": len(settings.ALLOWED_HOSTS) > 0,
        }

        self.stdout.write("\n" + "=" * 50)
        for key, value in checks.items():
            status = self.style.SUCCESS("✓") if value else self.style.ERROR("✗")
            self.stdout.write(
                f'{status} {key}: {"Configurado" if value else "NO configurado"}'
            )

        self.stdout.write("=" * 50 + "\n")

        if not all(checks.values()):
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠ Algunas variables no están configuradas."
                    "\nRevisa tu archivo .env"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✓ Todas las variables están configuradas correctamente"
                )
            )
