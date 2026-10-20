# --- my_project/domain/review.py ---

class Review:
    """
    Клас-модель, що представляє відгук.
    """
    def __init__(self, id, rating, comment, created_at, Users_id, Products_id):
        self.id = id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.Users_id = Users_id
        self.Products_id = Products_id

    def to_dict(self):
        """Перетворює об'єкт Review на словник (для JSON)."""
        return {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "users_id": self.Users_id,
            "products_id": self.Products_id
        }