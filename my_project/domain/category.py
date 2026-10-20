class Category:
    """
    Клас-модель, що представляє категорію.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        """Перетворює об'єкт Category на словник (для JSON)."""
        return {
            "id": self.id,
            "name": self.name
        }