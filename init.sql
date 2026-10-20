SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

CREATE SCHEMA IF NOT EXISTS `ecommerce_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ecommerce_db`;

DROP TABLE IF EXISTS `reviews`;
DROP TABLE IF EXISTS `products_has_attributes`;
DROP TABLE IF EXISTS `orderitems`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `cartitems`;
DROP TABLE IF EXISTS `cart`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `subcategories`;
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `attributes`;

CREATE TABLE IF NOT EXISTS `attributes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(100),
  `email` VARCHAR(100) NOT NULL,
  `password_hash` VARCHAR(250),
  `phone` VARCHAR(20),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `email_idx` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `subcategories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Categories_id` INT NOT NULL,
  `name` VARCHAR(50),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`Categories_id`) REFERENCES `categories` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200),
  `description` TEXT,
  `price` DECIMAL(10,2),
  `stock_quantity` INT,
  `Subcategories_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `price_idx` (`price`),
  INDEX `name_idx` (`name`),
  FOREIGN KEY (`Subcategories_id`) REFERENCES `subcategories` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `cart` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Users_id` INT NOT NULL,
  `total_quantity` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`Users_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Users_id` INT NOT NULL,
  `order_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `status` VARCHAR(70) DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  INDEX `order_date_idx` (`order_date`),
  FOREIGN KEY (`Users_id`) REFERENCES `users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `cartitems` (
  `Cart_id` INT NOT NULL,
  `Products_id` INT NOT NULL,
  `quantity` INT,
  `price` DECIMAL(10,2),
  PRIMARY KEY (`Cart_id`, `Products_id`),
  FOREIGN KEY (`Cart_id`) REFERENCES `cart` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Products_id`) REFERENCES `products` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `orderitems` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Orders_id` INT NOT NULL,
  `Products_id` INT NOT NULL,
  `quantity` INT,
  `price` DECIMAL(10,2),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`Orders_id`) REFERENCES `orders` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`Products_id`) REFERENCES `products` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `products_has_attributes` (
  `Products_id` INT NOT NULL,
  `Attributes_id` INT NOT NULL,
  `value` VARCHAR(100),
  PRIMARY KEY (`Products_id`, `Attributes_id`),
  FOREIGN KEY (`Attributes_id`) REFERENCES `attributes` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Products_id`) REFERENCES `products` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rating` INT,
  `comment` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `Users_id` INT NOT NULL,
  `Products_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `rating_idx` (`rating`),
  FOREIGN KEY (`Products_id`) REFERENCES `products` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Users_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `phone_idx` ON `users` (`phone`);
CREATE INDEX `stock_quantity_idx` ON `products` (`stock_quantity`);

INSERT INTO `attributes` (`id`, `name`) VALUES
(1, 'Колір'), (2, 'Розмір'), (3, 'Матеріал'), (4, 'Автор'), (5, 'Розмір екрану'),
(6, 'Вага'), (7, 'Виробник'), (8, 'Рік видання'), (9, 'Об\'єм пам\'яті'), (10, 'Тип');

INSERT INTO `users` (`id`, `full_name`, `email`, `password_hash`, `phone`) VALUES
(1, 'Іван Іванов', 'ivan@example.com', 'hash123', '0501112233'),
(2, 'Петро Петренко', 'petro@example.com', 'hash456', '0672223344'),
(3, 'Марія Сидоренко', 'maria@example.com', 'hash789', '0933334455'),
(4, 'Олена Ковальчук', 'olena@example.com', 'hash101', '0504445566'),
(5, 'Андрій Мельник', 'andriy@example.com', 'hash112', '0675556677'),
(6, 'Сергій Бондаренко', 'serhiy@example.com', 'hash131', '0936667788'),
(7, 'Наталія Шевченко', 'nataliia@example.com', 'hash415', '0507778899'),
(8, 'Віктор Кравченко', 'viktor@example.com', 'hash161', '0678889900'),
(9, 'Юлія Поліщук', 'yuliia@example.com', 'hash718', '0939990011'),
(10, 'Олександр Ткаченко', 'oleksandr@example.com', 'hash191', '0500001122'),
(11, 'Дмитро Коваленко', 'dmytro@example.com', 'hash202', '0671112233'),
(12, 'Ірина Захарченко', 'iryna@example.com', 'hash303', '0932223344');

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Електроніка'), (2, 'Книги'), (3, 'Одяг'), (4, 'Дім та Сад'), (5, 'Спорт'),
(6, 'Дитячі товари'), (7, 'Краса та Здоров\'я'), (8, 'Автотовари'), (9, 'Інструменти'), (10, 'Побутова техніка');

INSERT INTO `subcategories` (`id`, `Categories_id`, `name`) VALUES
(1, 1, 'Смартфони'), (2, 1, 'Ноутбуки'), (3, 1, 'Телевізори'),
(4, 2, 'Художня література'), (5, 2, 'Наукова література'), (6, 3, 'Футболки'),
(7, 3, 'Джинси'), (8, 4, 'Меблі'), (9, 4, 'Садовий інвентар'),
(10, 5, 'Велосипеди'), (11, 10, 'Холодильники'), (12, 10, 'Пральні машини'),
(13, 1, 'Навушники'), (14, 2, 'Комікси'), (15, 3, 'Взуття');

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock_quantity`, `Subcategories_id`) VALUES
(1, 'Смартфон "Alpha X"', 'Новітній смартфон з 128ГБ', 24999.99, 100, 1),
(2, 'Ноутбук "Legion Pro"', 'Ігровий ноутбук 16GB RAM', 45000.00, 50, 2),
(3, 'Телевізор "Vision 55"', '55-дюймовий 4K Smart TV', 18999.00, 75, 3),
(4, 'Книга "Загублений світ"', 'Пригодницький роман', 350.50, 200, 4),
(5, 'Книга "Історія Всесвіту"', 'Науково-популярна', 420.00, 150, 5),
(6, 'Футболка "Basic Cotton"', 'Біла бавовняна футболка', 299.00, 500, 6),
(7, 'Джинси "Slim Fit"', 'Сині джинси', 1200.00, 300, 7),
(8, 'Диван "Комфорт"', 'Тримісний розкладний диван', 15000.00, 40, 8),
(9, 'Набір садових інструментів', 'Лопата, граблі, секатор', 899.99, 120, 9),
(10, 'Гірський велосипед "Rider"', '21 швидкість, алюм. рама', 9500.00, 30, 10),
(11, 'Холодильник "Frosty"', 'Двокамерний, No Frost', 16500.00, 60, 11),
(12, 'Пральна машина "CleanMax"', 'Завантаження 7 кг', 11200.00, 80, 12),
(13, 'Бездротові навушники "Air"', 'З шупомоглинанням', 4500.00, 110, 13),
(14, 'Смартфон "Beta Y"', 'Бюджетна модель', 8999.00, 150, 1),
(15, 'Кросівки "Runner 2.0"', 'Для бігу', 2100.00, 250, 15);

INSERT INTO `cart` (`id`, `Users_id`, `total_quantity`) VALUES
(1, 1, 3), (2, 2, 1), (3, 3, 2), (4, 4, 0), (5, 5, 1), (6, 6, 4),
(7, 7, 1), (8, 8, 0), (9, 9, 2), (10, 10, 1), (11, 11, 1), (12, 12, 0);

INSERT INTO `cartitems` (`Cart_id`, `Products_id`, `quantity`, `price`) VALUES
(1, 1, 1, 24999.99), (1, 6, 2, 299.00), (2, 4, 1, 350.50), (3, 10, 1, 9500.00),
(3, 15, 1, 2100.00), (5, 2, 1, 45000.00), (6, 7, 2, 1200.00), (6, 6, 2, 299.00),
(7, 13, 1, 4500.00), (9, 3, 1, 18999.00), (9, 14, 1, 8999.00), (10, 11, 1, 16500.00),
(11, 8, 1, 15000.00);

INSERT INTO `orders` (`id`, `Users_id`, `status`) VALUES
(1, 1, 'Completed'), (2, 2, 'Shipped'), (3, 3, 'Processing'), (4, 5, 'Completed'),
(5, 7, 'Pending'), (6, 1, 'Cancelled'), (7, 9, 'Shipped'), (8, 10, 'Completed'),
(9, 2, 'Processing'), (10, 6, 'Completed');

INSERT INTO `orderitems` (`id`, `Orders_id`, `Products_id`, `quantity`, `price`) VALUES
(1, 1, 2, 1, 45000.00), (2, 1, 7, 1, 1200.00), (3, 2, 4, 2, 350.50),
(4, 3, 10, 1, 9500.00), (5, 4, 14, 1, 8999.00), (6, 5, 13, 1, 4500.00),
(7, 6, 6, 5, 299.00), (8, 7, 3, 1, 18999.00), (9, 8, 11, 1, 16500.00),
(10, 9, 5, 1, 420.00), (11, 9, 4, 1, 350.50), (12, 10, 8, 1, 15000.00),
(13, 10, 6, 3, 299.00);

INSERT INTO `products_has_attributes` (`Products_id`, `Attributes_id`, `value`) VALUES
(1, 1, 'Чорний'), (1, 5, '6.7 дюймів'), (1, 9, '128 ГБ'), (2, 1, 'Сірий'),
(2, 7, 'Lenovo'), (2, 5, '16 дюймів'), (4, 4, 'Артур Конан Дойл'), (4, 8, '2021'),
(5, 4, 'Стівен Гокінг'), (6, 1, 'Білий'), (6, 2, 'L'), (6, 3, 'Бавовна'),
(7, 2, '32/34'), (10, 1, 'Червоний'), (11, 7, 'Samsung');

INSERT INTO `reviews` (`id`, `rating`, `comment`, `Users_id`, `Products_id`) VALUES
(1, 5, 'Чудовий телефон, швидка доставка!', 1, 1),
(2, 4, 'Ноутбук потужний, але трохи шумить', 5, 2),
(3, 5, 'Книга прийшла в ідеальному стані.', 2, 4),
(4, 3, 'Футболка нормальна, але розмір трохи завеликий', 6, 6),
(5, 5, 'Дуже зручний велосипед!', 3, 10),
(6, 4, 'Гарний телевізор за свою ціну', 9, 3),
(7, 2, 'Дуже складна книга, не для всіх', 2, 5),
(8, 5, 'Найкращі навушники, які в мене були', 7, 13),
(9, 4, 'Джинси сіли ідеально', 1, 7),
(10, 5, 'Холодильник працює тихо, морозить добре', 10, 11);

SET FOREIGN_KEY_CHECKS=1;




-- скрипт, таблиці а потім діаграма згенерована на остнові цього скрипта
-- це для звіту