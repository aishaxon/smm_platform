import random

from .models import TelegramOTP
from apps.users.models import User


def find_user_by_phone(phone: str):
    return User.objects.filter(phone=phone).first()


def generate_otp(phone: str) -> str:
    code = f"{random.randint(100000, 999999)}"
    TelegramOTP.objects.create(phone=phone, code=code)
    return code


def verify_otp(phone: str, code: str) -> bool:
    otp = (
        TelegramOTP.objects.filter(phone=phone, code=code, is_verified=False)
        .order_by("-created_at")
        .first()
    )
    if not otp or otp.is_expired():
        return False
    otp.is_verified = True
    otp.save(update_fields=["is_verified"])
    return True


def attach_telegram_and_set_password(user: User, telegram_id: int, new_password: str):
    user.telegram_id = telegram_id
    user.set_password(new_password)
    user.save(update_fields=["telegram_id", "password"])
