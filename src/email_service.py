import copy
from datetime import datetime
from typing import List
from src.email_models import Email, Status


class EmailService:
    """Сервис для отправки email сообщений"""

    def __init__(self, email: Email):
        self.email = email

    def send_email(self) -> List[Email]:
        """
        Имитирует отправку письма.
        Возвращает список писем (по одному на каждого получателя).

        Returns:
            List[Email]: Список отправленных писем
        """
        # Создаем копию для работы
        email_copy = copy.deepcopy(self.email)

        # Подготавливаем письмо если нужно
        if email_copy.status != Status.READY:
            email_copy.prepare()

        # Исправление: если нет получателей, возвращаем пустой список
        if not email_copy.recipients or len(email_copy.recipients) == 0:
            return []

        sent_emails = []

        for recipient in email_copy.recipients:
            # Создаем глубокую копию письма для каждого получателя
            email_for_recipient = copy.deepcopy(email_copy)

            # Оставляем только одного получателя
            email_for_recipient.recipients = [recipient]

            # Устанавливаем дату отправки
            email_for_recipient.date = datetime.now()

            # Меняем статус
            if email_copy.status == Status.READY:
                email_for_recipient.status = Status.SENT
            else:
                email_for_recipient.status = Status.FAILED

            sent_emails.append(email_for_recipient)

        return sent_emails