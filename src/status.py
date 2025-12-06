from enum import StrEnum


class Status(StrEnum):
    """Статусы письма"""

    DRAFT = "draft"  # Черновик
    READY = "ready"  # Готово к отправке
    SENT = "sent"  # Отправлено
    FAILED = "failed"  # Ошибка отправки
    INVALID = "invalid"  # Невалидное письмо
