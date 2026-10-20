class User:
    """
    Клас-модель, що представляє користувача.
    """
    def __init__(self, id, full_name, email, password_hash, phone, created_at):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
        self.created_at = created_at

    def to_dict(self):
        """Перетворює об'єкт User на словник (для JSON)."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            # Ніколи не повертаємо хеш пароля у відповіді API
            # "password_hash": self.password_hash, 
            "phone": self.phone,
            # datetime з БД треба конвертувати у str (isoformat) для JSON
            "created_at": self.created_at.isoformat() if self.created_at else None
        }