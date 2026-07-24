# SMM Platform - Backend (Klassik Django REST Framework)

SMM kompaniyasi uchun ichki boshqaruv tizimi. 4 rol: CEO, Project Manager, Employee, Client.
Docker, Celery, Redis kerak emas - `python manage.py runserver` bilan ishlaydi.

## Texnologiyalar
- Django 5 + Django REST Framework
- SQLite (standart, hech narsa o'rnatish shart emas)
- JWT autentifikatsiya (simplejwt)
- Telegram bot - oddiy `requests` bilan long polling (aiogram/asyncio kerak emas)
- drf-spectacular (Swagger/OpenAPI docs)

## Ishga tushirish

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser    # bu CEO bo'ladi

python manage.py runserver
```

- Admin panel: http://127.0.0.1:8000/admin/
- Swagger docs: http://127.0.0.1:8000/api/docs/

## Telegram bot (ixtiyoriy, keyinroq ham qo'shsa bo'ladi)

1. BotFather'dan token oling
2. `config/settings.py` faylida `TELEGRAM_BOT_TOKEN` ni to'ldiring (yoki muhit o'zgaruvchisi orqali bering)
3. Alohida terminalda:
   ```bash
   python manage.py runbot
   ```

## Asosiy API yo'nalishlari

| Endpoint | Rol | Vazifasi |
|---|---|---|
| `POST /api/token/` | hammasi | login (username/password) |
| `GET /api/users/employees/me/` | hammasi | o'z profili |
| `POST /api/users/employees/create_employee/` | CEO | xodim qo'shish |
| `POST /api/users/employees/{id}/set_permissions/` | CEO | ruxsat berish |
| `GET/POST /api/projects/` | CEO/PM | loyihalar |
| `GET/POST /api/stages/` | rolga qarab filtrlangan | bosqichlar |
| `POST /api/stages/{id}/start/` | tayinlangan xodim | bosqichni boshlash |
| `POST /api/stages/{id}/complete/` | tayinlangan xodim | bosqichni yakunlash |
| `POST /api/salary/calculate/{user_id}/{year}/{month}/` | CEO | oylik hisoblash |
| `GET /api/salary/my/` | xodim | o'z oyligi |
| `GET /api/notifications/` | hammasi | o'z bildirishnomalari |
| `GET /api/clients/my-projects/` | client | o'z loyihalari progressi |

## Muhim arxitektura qarori

Ruxsatlar (permissions) har bir `ViewSet.get_queryset()` darajasida filtrlanadi -
frontendda yashirish YETARLI EMAS. Masalan `apps/stages/views.py` dagi
`StageViewSet.get_queryset()` metodiga qarang.

## Test qilish tartibi (Postman/Swagger orqali)

1. Superuser bilan login qiling (`/api/token/`) - bu CEO
2. `/api/users/employees/create_employee/` orqali PM va employee qo'shing
3. `/api/projects/` orqali loyiha yarating (client sifatida ham bitta user kerak, role="client")
4. `/api/stages/` orqali bosqich yarating, `assigned_to` va `required_permission` bilan
5. Employee sifatida login qilib `/api/stages/{id}/start/` va `/complete/` chaqiring
6. CEO sifatida `/api/salary/calculate/{user_id}/{year}/{month}/` chaqirib oylikni hisoblang
# smm_platform
# smm_platform
# smm_platform
