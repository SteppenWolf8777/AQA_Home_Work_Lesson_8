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
    sender: EmailAddress
    recipients: Union[EmailAddress, List[EmailAddress]]
    status: Status = Status.DRAFT
    date: Optional[datetime] = None
    short_body: Optional[str] = None

    def __post_init__(self):
        """Приводит получателей к списку EmailAddress"""
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]

    def _clean_text(self, text: str) -> str:
        """Очищает текст от лишних пробелов и переносов"""
        text = text.replace("\n", " ").replace("\t", " ")
        words = text.split()
        return " ".join(words)

    def add_short_body(self, length: int = 50) -> None:
        """Формирует сокращенную версию тела письма"""

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



