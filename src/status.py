from enum import StrEnum


class Status(StrEnum):
    """Статусы письма"""
    DRAFT = "Черновик"
    READY = "Готово к отправке"
    SENT = "Отправлено"
    FAILED = "Ошибка отправки"
    INVALID = "Невалидное письмо"