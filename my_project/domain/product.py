# --- my_project/domain/product.py ---
from my_project.domain.subcategory import Subcategory 

class Product:
    """
    Клас-модель, що представляє товар.
    Тепер він "вміє" зберігати повну інформацію про свою підкатегорію.
    """
    
    # Оновлений __init__ для прийому "ланцюгових" даних
    def __init__(self, id, name, description, price, stock_quantity, Subcategories_id, 
                 subcategory_name=None, Categories_id=None, category_name=None): 
        
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        
        # Ми створюємо "вкладений" об'єкт Subcategory всередині Product
        # і передаємо йому дані про його батьківську категорію
        if Subcategories_id is not None:
            self.subcategory = Subcategory(id=Subcategories_id, 
                                           Categories_id=Categories_id, 
                                           name=subcategory_name, 
                                           category_name=category_name)
        else:
            self.subcategory = None

    def to_dict(self):
        """Перетворює об'єкт Product на словник (для JSON)."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # DECIMAL з БД треба конвертувати у float для JSON
            "price": float(self.price) if self.price is not None else None,
            "stock_quantity": self.stock_quantity,
            
            # Повертаємо цілий вкладений об'єкт
            "subcategory": self.subcategory.to_dict() if self.subcategory else None
        }