from django.conf import settings
from .models import Notification


def notify_user(user_id: int, message: str, notif_type: str) -> Notification:
    notif = Notification.objects.create(user_id=user_id, message=message, notif_type=notif_type)

    from apps.users.models import User
    user = User.objects.filter(id=user_id).first()
    if user and user.telegram_id and settings.TELEGRAM_BOT_TOKEN:
        if _send_telegram_message(user.telegram_id, message):
            notif.sent_via_telegram = True
            notif.save(update_fields=["sent_via_telegram"])

    return notif


def _send_telegram_message(telegram_id: int, text: str) -> bool:
    import requests

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": telegram_id, "text": text}, timeout=5)
        return response.ok
    except requests.RequestException:
        return False


def get_unread_count(user) -> int:
    return Notification.objects.filter(user=user, is_read=False).count()
