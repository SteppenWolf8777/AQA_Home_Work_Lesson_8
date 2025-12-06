from datetime import datetime
from typing import List

from virtualenv.seed.embed.via_app_data.pip_install import copy

from src.dataclass_email import Email
from src.status import Status


class EmailService:
    """Сервис для отправки email сообщений"""

    @staticmethod
    def send_email(email: Email) -> List[Email]:
        """
                Имитирует отправку письма.
                Возвращает список писем (по одному на каждого получателя).

                Args:
                    email: Письмо для отправки

                Returns:
                    List[Email]: Список отправленных писем

                Raises:
                    ValueError: Если письмо не готово к отправке
                """
        # Проверяем, что письмо подготовлено
        if email.status != Status.READY:
            email.prepare()

        if not email.is_valid():
            raise ValueError("Письмо не готово к отправке. Проверьте тему, тело, отправителя и получателей.")

        sent_emails: []

        for recipient in email.recipients:
            # Создаем копию письма для каждого получателя
            email_copy = copy.deepcopy(email)

            # Оставляем только одного получателя
            email_copy.recipients = [recipient]

            # Устанавливаем дату отправки
            email_copy.date = datetime.now()

            # Меняем статус
            if email.status == Status.READY:
                email_copy.status = Status.SENT
            else:
                email_copy.status = Status.FAILED

            sent_emails.append(email_copy)

        return sent_emails

    @staticmethod
    def send_multiple_emails(emails: List[Email]) -> List[List[Email]]:
        """
        Отправляет несколько писем

        Args:
            emails: Список писем для отправки

        Returns:
            List[List[Email]]: Список списков отправленных писем
        """
        results = []
        for email in emails:
            try:
                sent = EmailService.send_email(email)
                results.append(sent)
            except ValueError as e:
                print(f"Ошибка при отправке письма: {e}")
                results.append([])

        return results


