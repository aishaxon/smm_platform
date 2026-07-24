from django.core.management.base import BaseCommand

from apps.telegram_bot.bot import run_polling


class Command(BaseCommand):
    help = "Telegram botni polling rejimida ishga tushiradi (aiogram/asyncio'siz, oddiy requests bilan)"

    def handle(self, *args, **options):
        run_polling()
