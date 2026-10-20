class Attribute:
    """
    Клас-модель, що представляє атрибут.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        """Перетворює об'єкт Attribute на словник (для JSON)."""
        return {
            "id": self.id,
            "name": self.name
        }