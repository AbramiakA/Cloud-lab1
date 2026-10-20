import os
from flask import Flask
from flask_cors import CORS
from my_project.database import get_db_connection, initialize_database

# 1. Створення Flask-додатку
app = Flask(__name__)
CORS(app) 

# 2. Реєстрація "креслень" (Blueprints) з маршрутами
from my_project.route.product_routes import products_bp
app.register_blueprint(products_bp, url_prefix='/api')

from my_project.route.user_routes import users_bp
app.register_blueprint(users_bp, url_prefix='/api')

from my_project.route.category_routes import categories_bp
app.register_blueprint(categories_bp, url_prefix='/api')

from my_project.route.attribute_routes import attributes_bp
app.register_blueprint(attributes_bp, url_prefix='/api')

from my_project.route.subcategory_routes import subcategories_bp
app.register_blueprint(subcategories_bp, url_prefix='/api')

from my_project.route.review_routes import reviews_bp
app.register_blueprint(reviews_bp, url_prefix='/api')

@app.route('/health', methods=['GET'])
def health():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()

        return {"status": "ok"}, 200

    except Exception:
        return {"status": "error"}, 503

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

initialize_database()

# 3. Головна точка входу
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)