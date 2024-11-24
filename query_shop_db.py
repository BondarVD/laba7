import psycopg2
from tabulate import tabulate

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


# Форматований вивід таблиці
def display_table(cursor, query, description):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(f"\n{description}:\n")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"Помилка виконання запиту: {e}")


# Виконання запитів
def execute_queries():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Вивести структуру та дані з таблиць
        tables = ["clients", "products", "sales"]
        for table in tables:
            print(f"\nТаблиця: {table.upper()}")
            display_table(cursor, f"SELECT * FROM {table};", f"Дані таблиці {table}")

        # Запит 1: Всі продажі, оплачені готівкою
        query1 = """
        SELECT s.sale_id, c.company_name, s.sale_date, p.product_name, s.quantity, s.discount, s.payment_method
        FROM sales s
        JOIN clients c ON s.client_id = c.client_id
        JOIN products p ON s.product_id = p.product_id
        WHERE s.payment_method = 'готівковий'
        ORDER BY c.company_name;
        """
        display_table(cursor, query1, "Продажі, оплачені готівкою")

        # Запит 2: Продажі з доставкою
        query2 = """
        SELECT s.sale_id, c.company_name, s.sale_date, p.product_name, s.quantity, s.delivery_needed, s.delivery_cost
        FROM sales s
        JOIN clients c ON s.client_id = c.client_id
        JOIN products p ON s.product_id = p.product_id
        WHERE s.delivery_needed = TRUE;
        """
        display_table(cursor, query2, "Продажі з доставкою")

        # Запит 3: Сума та сума зі знижкою для кожного клієнта
        query3 = """
        SELECT c.company_name, 
               SUM(s.quantity * p.price) AS total_sum, 
               SUM(s.quantity * p.price * (1 - s.discount / 100)) AS total_with_discount
        FROM sales s
        JOIN clients c ON s.client_id = c.client_id
        JOIN products p ON s.product_id = p.product_id
        GROUP BY c.company_name;
        """
        display_table(cursor, query3, "Сума та сума зі знижкою для кожного клієнта")

        # Запит 4: Усі покупки клієнта (запит із параметром)
        client_name = input("\nВведіть назву клієнта для пошуку його покупок: ")
        query4 = f"""
        SELECT s.sale_id, s.sale_date, p.product_name, s.quantity, s.discount
        FROM sales s
        JOIN clients c ON s.client_id = c.client_id
        JOIN products p ON s.product_id = p.product_id
        WHERE c.company_name = %s;
        """
        cursor.execute(query4, (client_name,))
        rows = cursor.fetchall()
        if rows:
            headers = [desc[0] for desc in cursor.description]
            print(f"\nПокупки клієнта {client_name}:\n")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print(f"\nНемає покупок для клієнта {client_name}.")

        # Запит 5: Кількість покупок для кожного клієнта
        query5 = """
        SELECT c.company_name, COUNT(s.sale_id) AS purchase_count
        FROM sales s
        JOIN clients c ON s.client_id = c.client_id
        GROUP BY c.company_name;
        """
        display_table(cursor, query5, "Кількість покупок для кожного клієнта")

        # Запит 6: Сума за готівковим та безготівковим розрахунком
        query6 = """
        SELECT c.company_name,
               SUM(CASE WHEN s.payment_method = 'готівковий' THEN s.quantity * p.price * (1 - s.discount / 100) ELSE 0 END) AS cash_sum,
               SUM(CASE WHEN s.payment_method = 'безготівковий' THEN s.quantity * p.price * (1 - s.discount / 100) ELSE 0 END) AS non_cash_sum
        FROM sales s
        JOIN clients c ON s.client_id = c.client_id
        JOIN products p ON s.product_id = p.product_id
        GROUP BY c.company_name;
        """
        display_table(cursor, query6, "Сума за готівковим та безготівковим розрахунком")

    except Exception as e:
        print(f"Помилка виконання запитів: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    execute_queries()
