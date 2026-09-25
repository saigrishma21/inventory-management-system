from app.db import get_connection


def add_inventory(product_id, warehouse_id, quantity, reorder_level):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO inventory
            (
                product_id,
                warehouse_id,
                quantity,
                reorder_level
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                product_id,
                warehouse_id,
                quantity,
                reorder_level
            )
        )

        connection.commit()
        print("Inventory record added.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def get_inventory():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            i.inventory_id,
            p.product_name,
            p.sku,
            w.warehouse_name,
            i.quantity,
            i.reorder_level
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        ORDER BY i.inventory_id
        """
    )

    rows = cursor.fetchall()

    print("\n--- Inventory ---")

    for row in rows:
        print(
            f"ID: {row[0]} | "
            f"Product: {row[1]} | "
            f"SKU: {row[2]} | "
            f"Warehouse: {row[3]} | "
            f"Quantity: {row[4]} | "
            f"Reorder Level: {row[5]}"
        )

    cursor.close()
    connection.close()


def update_inventory(inventory_id, quantity, reorder_level):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE inventory
            SET quantity = %s,
                reorder_level = %s
            WHERE inventory_id = %s
            """,
            (
                quantity,
                reorder_level,
                inventory_id
            )
        )

        connection.commit()
        print("Inventory updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def delete_inventory(inventory_id):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM inventory
            WHERE inventory_id = %s
            """,
            (inventory_id,)
        )

        connection.commit()
        print("Inventory deleted successfully.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()