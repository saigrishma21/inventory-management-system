from app.db import get_connection


def add_supplier(name, email, phone, address):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO suppliers
            (supplier_name, email, phone, address)
            VALUES (%s, %s, %s, %s)
            RETURNING supplier_id
            """,
            (name, email, phone, address)
        )

        supplier_id = cursor.fetchone()[0]
        connection.commit()

        print(f"Supplier added successfully. ID: {supplier_id}")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def get_suppliers():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT supplier_id,
               supplier_name,
               email,
               phone,
               address
        FROM suppliers
        ORDER BY supplier_id
        """
    )

    rows = cursor.fetchall()

    print("\n--- Suppliers ---")

    for row in rows:
        print(row)

    cursor.close()
    connection.close()


def update_supplier(supplier_id, name, email, phone, address):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE suppliers
            SET supplier_name = %s,
                email = %s,
                phone = %s,
                address = %s
            WHERE supplier_id = %s
            """,
            (name, email, phone, address, supplier_id)
        )

        connection.commit()
        print("Supplier updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()

def delete_supplier(supplier_id):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT supplier_name
            FROM suppliers
            WHERE supplier_id = %s
        """, (supplier_id,))

        supplier = cursor.fetchone()

        if not supplier:
            print("Supplier not found.")
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM purchases
            WHERE supplier_id = %s
        """, (supplier_id,))

        purchase_count = cursor.fetchone()[0]

        if purchase_count > 0:
            print("Supplier cannot be deleted.")
            print("Supplier is being used by existing purchase records.")
            print("Purchase records:", purchase_count)
            return

        cursor.execute("""
            DELETE FROM suppliers
            WHERE supplier_id = %s
        """, (supplier_id,))

        connection.commit()

        print("Supplier deleted successfully.")

    except Exception as error:
        connection.rollback()
        print("Supplier deletion failed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()