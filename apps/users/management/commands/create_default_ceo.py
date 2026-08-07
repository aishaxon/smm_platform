import os

from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    help = "Muhit o'zgaruvchilaridan CEO superuser yaratadi (agar hali yo'q bo'lsa)"

    def handle(self, *args, **options):
        username = os.environ.get("DEFAULT_CEO_USERNAME")
        password = os.environ.get("DEFAULT_CEO_PASSWORD")
        phone = os.environ.get("DEFAULT_CEO_PHONE")
        email = os.environ.get("DEFAULT_CEO_EMAIL", "")

        if not username or not password or not phone:
            self.stdout.write(self.style.WARNING(
                "DEFAULT_CEO_USERNAME / DEFAULT_CEO_PASSWORD / DEFAULT_CEO_PHONE "
                "muhit o'zgaruvchilari sozlanmagan - o'tkazib yuborilyapti."
            ))
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"phone": phone, "email": email, "role": "ceo"},
        )

        if created:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.role = "ceo"
            user.save()
            self.stdout.write(self.style.SUCCESS(f"CEO yaratildi: {username}"))
        else:
            user.set_password(password)
            user.role = "ceo"
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"CEO yangilandi: {username}"))