FOR POSTMAN
Базова URL-адреса (Base URL): http://127.0.0.1:5000/api

1. CRUD: Users (Користувачі)

GET (всі): GET /api/users
___________________________

GET (один): GET /api/users/1
___________________________

POST (створити): POST /api/users
Body (JSON):

JSON
{
  "full_name": "Новий Юзер",
  "email": "user@example.com",
  "password_hash": "some_hash",
  "phone": "0501234567"
}
___________________________
PUT (оновити): PUT /api/users/1
Body (JSON):

JSON
{
  "full_name": "Ім'я Оновлено",
  "phone": "0997654321"
}
___________________________
DELETE (видалити): DELETE /api/users/1
______________________________________________________

2. CRUD: Products (Товари)
GET (всі): GET /api/products
___________________________
GET (один): GET /api/products/1
___________________________
POST (створити): POST /api/products
Body (JSON):

JSON
{
  "name": "Новий Товар",
  "description": "Опис...",
  "price": 99.99,
  "stock_quantity": 10,
  "Subcategories_id": 1
}
___________________________
PUT (оновити): PUT /api/products/1
Body (JSON):

JSON
{
  "price": 120.00,
  "stock_quantity": 5
}
___________________________
DELETE (видалити): DELETE /api/products/1
______________________________________________________

3. CRUD: Categories (Категорії)

GET (всі): GET /api/categories
___________________________
GET (одна): GET /api/categories/1
___________________________

POST (створити): POST /api/categories Body (JSON):

JSON
{
  "name": "Нова Категорія"
}
___________________________
PUT (оновити): PUT /api/categories/1 Body (JSON):

JSON
{
  "name": "Оновлена Категорія"
}
___________________________
DELETE (видалити): DELETE /api/categories/1
______________________________________________________

4. CRUD: Subcategories (Підкатегорії)
GET (всі): GET /api/subcategories
___________________________
GET (одна): GET /api/subcategories/1
___________________________
POST (створити): POST /api/subcategories Body (JSON):

JSON
{
  "name": "Нова Підкатегорія",
  "Categories_id": 1
}
___________________________
PUT (оновити): PUT /api/subcategories/1 Body (JSON):

JSON
{
  "name": "Оновлена Підкатегорія"
}
___________________________
DELETE (видалити): DELETE /api/subcategories/1
______________________________________________________

5. CRUD: Attributes (Атрибути)

GET (всі): GET /api/attributes
___________________________
GET (один): GET /api/attributes/1
___________________________
POST (створити): POST /api/attributes Body (JSON):

JSON
{
  "name": "Новий Атрибут (напр. Вага)"
}
___________________________
PUT (оновити): PUT /api/attributes/1 Body (JSON):

JSON
{
  "name": "Оновлений Атрибут"
}
___________________________
DELETE (видалити): DELETE /api/attributes/1
______________________________________________________

6. CRUD: Reviews (Відгуки)

GET (всі): GET /api/reviews
___________________________
GET (один): GET /api/reviews/1
___________________________
POST (створити): POST /api/reviews Body (JSON):

JSON
{
  "rating": 5,
  "comment": "Дуже сподобалось!",
  "Users_id": 1,
  "Products_id": 1
}
___________________________
PUT (оновити): PUT /api/reviews/1 Body (JSON):

JSON
{
  "comment": "Оновлений коментар."
}
___________________________
DELETE (видалити): DELETE /api/reviews/1
______________________________________________________

7. Тестування Зв'язків M:1 (Багато-до-Одного)
Підкатегорія + Категорія: GET /api/subcategories/1 
___________________________
Товар + Підкатегорія + Категорія: Запит: GET /api/products/1 
______________________________________________________
8. Тестування Зв'язків M:M (Багато-до-Багатьох)

Тест 1 (Read): Отримати атрибути товару Запит: GET /api/products/1/attributes
___________________________
Тест 2 (Create): Призначити атрибут товару Запит: POST /api/products/1/attributes Body (JSON):

JSON
{
  "attribute_id": 2,
  "value": "XL"
}
___________________________
Тест 3 (Update): Оновити значення атрибута Запит: PUT /api/products/1/attributes/2 Body (JSON):

JSON
{
  "value": "XXL"
}
___________________________
Тест 4 (Delete): Видалити атрибут з товару Запит: DELETE /api/products/1/attributes/2