from enum import StrEnum, auto


class Status(StrEnum):
    """Статусы письма"""
    DRAFT = auto()  # Черновик
    READY = auto()  # Готово к отправке
    SENT = auto()  # Отправлено
    FAILED = auto()  # Ошибка отправки
    INVALID = auto()  # Невалидное письмо