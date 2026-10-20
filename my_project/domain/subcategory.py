# --- my_project/domain/subcategory.py ---
from my_project.domain.category import Category # <-- ДОДАЙ ЦЕЙ ІМПОРТ

class Subcategory:
    """
    Клас-модель, що представляє підкатегорію.
    """
    def __init__(self, id, Categories_id, name, category_name=None): # <-- ЗМІНА ТУТ
        self.id = id
        self.name = name
        
        # Створюємо вкладений об'єкт Category
        if Categories_id is not None:
            self.category = Category(Categories_id, category_name)
        else:
            self.category = None


    def to_dict(self):
        """Перетворює об'єкт Subcategory на словник (для JSON)."""
        return {
            "id": self.id,
            "name": self.name,
            # Повертаємо цілий об'єкт категорії
            "category": self.category.to_dict() if self.category else None
        }