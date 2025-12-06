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
        if '@' not in self._normalized:
            return self._normalized

        local_part, domain = self._normalized.split('@', 1)
        if len(local_part) < 2:
            masked_local = local_part + "***"
        else:
            masked_local = local_part[:2] + "***"

        return f"{masked_local}@{domain}"

    @property
    def login(self) -> str:
        """Возвращает логин (часть до @)"""
        if '@' in self._normalized:
            return self._normalized.split('@',1)[0]
        return ""

    @property
    def domain(self) -> str:
        """Возвращает домен (часть после @)"""
        if '@' in self._normalized:
            return self._normalized.split('@',1)[1]
        return ""

    def __str__(self) -> str:
        """Строковое представление - нормализованный адрес"""
        return self._normalized

    def __repr__(self) -> str:
        """Представление для отладки"""
        return f"EmailAddress('self._original')"

    def __eq__(self, other) -> bool:
        """Сравнение адресов по нормализованному значению"""
        if isinstance(other, EmailAddress):
            return self._normalized == other._normalized
        elif isinstance(other, str):
            return self._normalized == self._normalize(other)
        return False

