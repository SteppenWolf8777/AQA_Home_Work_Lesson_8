class EmailAddress:
    """Класс для работы с email адресами"""
    def __init__(self, address: str):
        self._original = address
        self._normalized = self._normalized(address)
        self._validate(self._normalized)

    @staticmethod
    def _normalized(address: str) -> str:
        if not address or not isinstance(address, str):
            return ""
        return address.lower().strip()

    @staticmethod
    def _validate(address: str):
        if not address:
            raise ValueError("Email адрес не может быть пустым")

        if '@' not in address:
            raise ValueError(f"Некорректный email адрес '{address}': отсутствует символ @")

        valid_domains = ['.com', '.ru', '.net']
        if not any(address.endswith(domain) for domain in valid_domains):
            raise ValueError(f"Некорректный email адрес '{address}': должен оканчиваться на .com, .ru или .net")

    @property
    def address(self) -> str:
        """Возвращает нормализованный адрес"""
        return self._normalized

    @property
    def masked(self) -> str:
        """Возвращает маскированный адрес в формате первые_2_символа + "***@" + домен"""
        login, domain = self._normalized.split('@', 1)
        return f"{login[:2]}***@{domain}"