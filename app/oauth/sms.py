from celery import shared_task


@shared_task
def send_otp(phone: str, opt: str):
    text = f"Ваш код подтверждения: {opt}"
    print(text, phone)
