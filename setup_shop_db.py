import psycopg2
from psycopg2 import sql

# Параметри підключення
DB_CONFIG = {
    "dbname": "shop_db",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432,
}

# Підключення до бази даних
def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Помилка підключення до БД: {e}")
        exit()

# Створення таблиць
def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Таблиця Клієнти
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            entity_type VARCHAR(50) CHECK (entity_type IN ('юридична', 'фізична')) NOT NULL,
            address TEXT NOT NULL,
            phone VARCHAR(15) NOT NULL,
            contact_person VARCHAR(50),
            account_number VARCHAR(20)
        );
        """)

        # Таблиця Товари
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
            stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
        );
        """)

        # Таблиця Продаж
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id SERIAL PRIMARY KEY,
            sale_date DATE NOT NULL DEFAULT CURRENT_DATE,
            client_id INTEGER REFERENCES clients(client_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            discount NUMERIC(5, 2) NOT NULL CHECK (discount BETWEEN 3 AND 20),
            payment_method VARCHAR(20) CHECK (payment_method IN ('готівковий', 'безготівковий')),
            delivery_needed BOOLEAN NOT NULL,
            delivery_cost NUMERIC(10, 2) DEFAULT 0
        );
        """)

        conn.commit()
        print("Таблиці створено успішно.")
    except Exception as e:
        print(f"Помилка створення таблиць: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Заповнення таблиць даними
def populate_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Дані для таблиці Клієнти
        cursor.execute("""
        INSERT INTO clients (company_name, entity_type, address, phone, contact_person, account_number)
        VALUES
            ('Фірма 1', 'юридична', 'Київ, вул. Хрещатик, 1', '0501234567', 'Іван Іванов', 'UA1234567890123456'),
            ('Фірма 2', 'юридична', 'Львів, вул. Дорошенка, 10', '0977654321', 'Олена Петрівна', 'UA0987654321098765'),
            ('Фізична особа 1', 'фізична', 'Одеса, вул. Дерибасівська, 5', '0931239876', 'Олег Олегович', NULL),
            ('Фізична особа 2', 'фізична', 'Харків, вул. Сумська, 15', '0679876543', 'Наталя Наталіївна', NULL);
        """)

        # Дані для таблиці Товари
        cursor.execute("""
        INSERT INTO products (product_name, price, stock_quantity)
        VALUES
            ('Товар 1', 100.00, 50),
            ('Товар 2', 200.00, 30),
            ('Товар 3', 300.00, 20),
            ('Товар 4', 400.00, 10),
            ('Товар 5', 500.00, 5),
            ('Товар 6', 600.00, 8),
            ('Товар 7', 700.00, 15),
            ('Товар 8', 800.00, 25),
            ('Товар 9', 900.00, 40),
            ('Товар 10', 1000.00, 60);
        """)

        # Дані для таблиці Продаж
        cursor.execute("""
        INSERT INTO sales (client_id, product_id, quantity, discount, payment_method, delivery_needed, delivery_cost)
        VALUES
            (1, 1, 2, 5, 'готівковий', TRUE, 50.00),
            (1, 2, 1, 10, 'готівковий', FALSE, 0),
            (2, 3, 3, 15, 'безготівковий', TRUE, 100.00),
            (3, 4, 1, 3, 'готівковий', FALSE, 0),
            (4, 5, 5, 20, 'безготівковий', TRUE, 150.00);
        """)

        conn.commit()
        print("Дані успішно додано.")
    except Exception as e:
        print(f"Помилка внесення даних: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
    populate_tables()
import psycopg2
from psycopg2 import sql

# Параметри підключення
DB_CONFIG = {
    "dbname": "shop_db",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432,
}

# Підключення до бази даних
def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Помилка підключення до БД: {e}")
        exit()

# Створення таблиць
def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Таблиця Клієнти
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            entity_type VARCHAR(50) CHECK (entity_type IN ('юридична', 'фізична')) NOT NULL,
            address TEXT NOT NULL,
            phone VARCHAR(15) NOT NULL,
            contact_person VARCHAR(50),
            account_number VARCHAR(20)
        );
        """)

        # Таблиця Товари
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
            stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
        );
        """)

        # Таблиця Продаж
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id SERIAL PRIMARY KEY,
            sale_date DATE NOT NULL DEFAULT CURRENT_DATE,
            client_id INTEGER REFERENCES clients(client_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            discount NUMERIC(5, 2) NOT NULL CHECK (discount BETWEEN 3 AND 20),
            payment_method VARCHAR(20) CHECK (payment_method IN ('готівковий', 'безготівковий')),
            delivery_needed BOOLEAN NOT NULL,
            delivery_cost NUMERIC(10, 2) DEFAULT 0
        );
        """)

        conn.commit()
        print("Таблиці створено успішно.")
    except Exception as e:
        print(f"Помилка створення таблиць: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Заповнення таблиць даними
def populate_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Дані для таблиці Клієнти
        cursor.execute("""
        INSERT INTO clients (company_name, entity_type, address, phone, contact_person, account_number)
        VALUES
            ('Фірма 1', 'юридична', 'Київ, вул. Хрещатик, 1', '0501234567', 'Іван Іванов', 'UA1234567890123456'),
            ('Фірма 2', 'юридична', 'Львів, вул. Дорошенка, 10', '0977654321', 'Олена Петрівна', 'UA0987654321098765'),
            ('Фізична особа 1', 'фізична', 'Одеса, вул. Дерибасівська, 5', '0931239876', 'Олег Олегович', NULL),
            ('Фізична особа 2', 'фізична', 'Харків, вул. Сумська, 15', '0679876543', 'Наталя Наталіївна', NULL);
        """)

        # Дані для таблиці Товари
        cursor.execute("""
        INSERT INTO products (product_name, price, stock_quantity)
        VALUES
            ('Товар 1', 100.00, 50),
            ('Товар 2', 200.00, 30),
            ('Товар 3', 300.00, 20),
            ('Товар 4', 400.00, 10),
            ('Товар 5', 500.00, 5),
            ('Товар 6', 600.00, 8),
            ('Товар 7', 700.00, 15),
            ('Товар 8', 800.00, 25),
            ('Товар 9', 900.00, 40),
            ('Товар 10', 1000.00, 60);
        """)

        # Дані для таблиці Продаж
        cursor.execute("""
        INSERT INTO sales (client_id, product_id, quantity, discount, payment_method, delivery_needed, delivery_cost)
        VALUES
            (1, 1, 2, 5, 'готівковий', TRUE, 50.00),
            (1, 2, 1, 10, 'готівковий', FALSE, 0),
            (2, 3, 3, 15, 'безготівковий', TRUE, 100.00),
            (3, 4, 1, 3, 'готівковий', FALSE, 0),
            (4, 5, 5, 20, 'безготівковий', TRUE, 150.00);
        """)

        conn.commit()
        print("Дані успішно додано.")
    except Exception as e:
        print(f"Помилка внесення даних: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
    populate_tables()
