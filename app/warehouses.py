from app.db import get_connection


def add_warehouse(name, location):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO warehouses
            (warehouse_name, location)
            VALUES (%s, %s)
            RETURNING warehouse_id
            """,
            (name, location)
        )

        warehouse_id = cursor.fetchone()[0]
        connection.commit()

        print(f"Warehouse added successfully. ID: {warehouse_id}")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def get_warehouses():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT warehouse_id,
               warehouse_name,
               location
        FROM warehouses
        ORDER BY warehouse_id
        """
    )

    rows = cursor.fetchall()

    print("\n--- Warehouses ---")

    for row in rows:
        print(row)

    cursor.close()
    connection.close()


def update_warehouse(warehouse_id, name, location):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE warehouses
            SET warehouse_name = %s,
                location = %s
            WHERE warehouse_id = %s
            """,
            (name, location, warehouse_id)
        )

        connection.commit()

        print("Warehouse updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def delete_warehouse(warehouse_id):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT warehouse_name
            FROM warehouses
            WHERE warehouse_id = %s
        """, (warehouse_id,))

        warehouse = cursor.fetchone()

        if not warehouse:
            print("Warehouse not found.")
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM inventory
            WHERE warehouse_id = %s
        """, (warehouse_id,))

        inventory_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM sales
            WHERE warehouse_id = %s
        """, (warehouse_id,))

        sales_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM purchases
            WHERE warehouse_id = %s
        """, (warehouse_id,))

        purchase_count = cursor.fetchone()[0]

        if inventory_count > 0 or sales_count > 0 or purchase_count > 0:
            print("Warehouse cannot be deleted.")
            print("Warehouse is being used by existing records.")
            print("Inventory records:", inventory_count)
            print("Sales records:", sales_count)
            print("Purchase records:", purchase_count)
            return

        cursor.execute("""
            DELETE FROM warehouses
            WHERE warehouse_id = %s
        """, (warehouse_id,))

        connection.commit()

        print("Warehouse deleted successfully.")

    except Exception as error:
        connection.rollback()
        print("Warehouse deletion failed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()