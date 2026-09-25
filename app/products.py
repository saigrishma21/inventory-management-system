from app.db import get_connection


def add_product(product_name, category_id, sku, unit_price):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO products
            (product_name, category_id, sku, unit_price)
            VALUES (%s, %s, %s, %s)
            RETURNING product_id
            """,
            (product_name, category_id, sku, unit_price)
        )

        product_id = cursor.fetchone()[0]
        connection.commit()

        print(f"Product added successfully. ID: {product_id}")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def get_products():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            p.product_id,
            p.product_name,
            p.sku,
            c.category_name,
            p.unit_price
        FROM products p
        JOIN categories c
            ON p.category_id = c.category_id
        ORDER BY p.product_id
        """
    )

    rows = cursor.fetchall()

    print("\n--- Products ---")

    for row in rows:
        print(
            f"ID: {row[0]} | "
            f"Name: {row[1]} | "
            f"SKU: {row[2]} | "
            f"Category: {row[3]} | "
            f"Price: {row[4]}"
        )

    cursor.close()
    connection.close()


def update_product(product_id, product_name, category_id, sku, unit_price):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE products
            SET product_name = %s,
                category_id = %s,
                sku = %s,
                unit_price = %s
            WHERE product_id = %s
            """,
            (
                product_name,
                category_id,
                sku,
                unit_price,
                product_id
            )
        )

        connection.commit()
        print("Product updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def delete_product(product_id):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT product_name
            FROM products
            WHERE product_id = %s
        """, (product_id,))

        product = cursor.fetchone()

        if not product:
            print("Product not found.")
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM inventory
            WHERE product_id = %s
        """, (product_id,))

        inventory_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM purchase_items
            WHERE product_id = %s
        """, (product_id,))

        purchase_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM sale_items
            WHERE product_id = %s
        """, (product_id,))

        sale_count = cursor.fetchone()[0]

        if inventory_count > 0 or purchase_count > 0 or sale_count > 0:
            print("Product cannot be deleted.")
            print("Product is being used by existing records.")
            print("Inventory records:", inventory_count)
            print("Purchase records:", purchase_count)
            print("Sales records:", sale_count)
            return

        cursor.execute("""
            DELETE FROM products
            WHERE product_id = %s
        """, (product_id,))

        connection.commit()

        print("Product deleted successfully.")

    except Exception as error:
        connection.rollback()
        print("Product deletion failed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()
