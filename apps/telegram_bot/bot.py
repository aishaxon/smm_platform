"""
Klassik variant: aiogram/asyncio kerak emas, faqat `requests` bilan
Telegram Bot API'ga oddiy HTTP so'rovlar (long polling).

Ishga tushirish: python manage.py runbot
"""
import re
import secrets
import time

import requests
from django.conf import settings

from .services import find_user_by_phone, generate_otp, verify_otp, attach_telegram_and_set_password

API_URL = "https://api.telegram.org/bot{token}/{method}"

# chat_id -> kutilayotgan telefon raqam (OTP tasdiqlanguncha)
_pending_phone: dict[int, str] = {}


def _call(method: str, **params):
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN sozlanmagan (config/settings.py yoki .env)")
    url = API_URL.format(token=token, method=method)
    response = requests.post(url, json=params, timeout=30)
    response.raise_for_status()
    return response.json()


def send_message(chat_id: int, text: str, reply_markup: dict | None = None):
    params = {"chat_id": chat_id, "text": text}
    if reply_markup:
        params["reply_markup"] = reply_markup
    return _call("sendMessage", **params)


def _contact_keyboard():
    return {
        "keyboard": [[{"text": "Telefon raqamni ulashish", "request_contact": True}]],
        "resize_keyboard": True,
        "one_time_keyboard": True,
    }


def _remove_keyboard():
    return {"remove_keyboard": True}


def handle_update(update: dict):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    contact = message.get("contact")

    if text == "/start":
        send_message(
            chat_id,
            "Xush kelibsiz! SMM platformasiga kirish uchun telefon raqamingizni ulashing.",
            reply_markup=_contact_keyboard(),
        )
        return

    if contact:
        phone = contact.get("phone_number", "")
        if not phone.startswith("+"):
            phone = f"+{phone}"

        user = find_user_by_phone(phone)
        if not user:
            send_message(
                chat_id,
                "Bu raqam tizimda topilmadi. Avval CEO sizni tizimga qo'shishi kerak.",
                reply_markup=_remove_keyboard(),
            )
            return

        code = generate_otp(phone)
        _pending_phone[chat_id] = phone
        # DIQQAT: demo uchun kod to'g'ridan-to'g'ri botga yozilmoqda.
        send_message(
            chat_id,
            f"Tasdiqlash kodi: {code}\nUshbu 6 xonali kodni shu yerga yozib yuboring.",
            reply_markup=_remove_keyboard(),
        )
        return

    if re.fullmatch(r"\d{6}", text or ""):
        phone = _pending_phone.get(chat_id)
        if not phone:
            send_message(chat_id, "Avval /start bosib telefon raqamingizni ulashing.")
            return

        if not verify_otp(phone, text):
            send_message(chat_id, "Kod noto'g'ri yoki muddati o'tgan. Qaytadan urinib ko'ring: /start")
            return

        user = find_user_by_phone(phone)
        new_password = secrets.token_urlsafe(6)
        attach_telegram_and_set_password(user, chat_id, new_password)
        _pending_phone.pop(chat_id, None)

        send_message(
            chat_id,
            "Tabriklaymiz! Hisobingiz faollashtirildi.\n"
            f"Login: {user.phone}\nParol: {new_password}\n"
            "Bu ma'lumotlarni saqlab qo'ying - ular orqali frontend/mobil ilovaga kirasiz.",
        )
        return

    send_message(chat_id, "Tushunmadim. /start buyrug'ini yuboring.")


def run_polling():
    """Cheksiz sikl - Ctrl+C bilan to'xtatiladi."""
    offset = None
    print("Bot polling rejimida ishga tushdi (to'xtatish uchun Ctrl+C)...")
    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset
            result = _call("getUpdates", **params)
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                handle_update(update)
        except requests.RequestException as exc:
            print(f"Xatolik: {exc}, 5 soniyadan keyin qayta urinamiz...")
            time.sleep(5)
