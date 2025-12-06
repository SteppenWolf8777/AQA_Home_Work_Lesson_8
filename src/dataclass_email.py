from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, List
from src.email_adress import EmailAddress
from src.status import Status


@dataclass
class Email:
    """Модель email письма"""

    subject: str
    body: str
    sender: Union[str, EmailAddress]
    recipients: Union[str, EmailAddress, List[Union[str, EmailAddress]]]
    status: Status = Status.DRAFT
    date: Optional[datetime] = None
    short_body: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания объекта"""
        # Конвертируем отправителя в EmailAddress если это строка
        if isinstance(self.sender, str):
            self.sender = EmailAddress(self.sender)

        # Конвертируем получателей в список EmailAddress
        self._normalize_recipients()

        # Инициализируем сокращенное тело если его нет
        if self.short_body is None:
            self.short_body = ""

    def _normalize_recipients(self):
        """Приводит получателей к списку EmailAddress"""
        if not self.recipients:
            self.recipients = []
        elif isinstance(self.recipients, (str, EmailAddress)):
            # Если один получатель, оборачиваем в список
            if isinstance(self.recipients, str):
                self.recipients = [EmailAddress(self.recipients)]
            else:
                self.recipients = [self.recipients]
        else:
            # Если список, конвертируем каждый элемент
            normalized = []
            for recipient in self.recipients:
                if isinstance(recipient, str):
                    normalized.append(EmailAddress(recipient))
                else:
                    normalized.append(recipient)
            self.recipients = normalized

    def _clean_text(self, text: str) -> str:
        """Очищает текст от лишних пробелов и переносов"""
        if not text:
            return ""
        # Заменяем табы и переводы строк на пробелы
        text = text.replace("\t", " ").replace("\n", " ")
        # Убираем лишние пробелы
        words = text.split()
        return " ".join(words)

    def add_short_body(self, length: int = 50) -> None:
        """Формирует сокращенную версию тела письма"""
        if not self.body:
            self.short_body = ""
            return

        cleaned_body = self._clean_text(self.body)
        if len(cleaned_body) <= length:
            self.short_body = cleaned_body
        else:
            self.short_body = cleaned_body[:length] + "..."

    def prepare(self) -> None:
        """
        Подготавливает письмо к отправке:
        1. Очищает тему и тело
        2. Проверяет валидность
        3. Создает сокращенную версию тела
        """
        # Очистка
        self.subject = self._clean_text(self.subject)
        self.body = self._clean_text(self.body)

        # Проверка валидности
        if self.subject and self.body and self.sender and self.recipients:
            self.status = Status.READY
        else:
            self.status = Status.INVALID

        # Создание сокращенного тела
        self.add_short_body()

    def is_valid(self) -> bool:
        """Проверяет, готово ли письмо к отправке"""
        return self.status == Status.READY

    def __repr__(self) -> str:
        """Строковое представление с маскированным отправителем"""
        sender_masked = (
            self.sender.masked
            if isinstance(self.sender, EmailAddress)
            else str(self.sender)
        )
        recipients_list = [str(r) for r in self.recipients]
        recipients_str = ", ".join(recipients_list)

        return (
            f"Кому: {recipients_str}\n"
            f"От: {sender_masked}\n"
            f"Тема: {self.subject}\n"
            f"Статус: {self.status}"
        )
