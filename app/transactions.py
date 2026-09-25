from app.db import get_connection


def create_sale(
    customer_name,
    product_id,
    warehouse_id,
    quantity
):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT inventory_id, quantity
            FROM inventory
            WHERE product_id = %s
            AND warehouse_id = %s
            FOR UPDATE
            """,
            (product_id, warehouse_id)
        )

        inventory = cursor.fetchone()

        if not inventory:
            raise Exception("Product is not available in this warehouse.")

        inventory_id = inventory[0]
        available_quantity = inventory[1]

        if available_quantity < quantity:
            raise Exception(
                f"Insufficient stock. Available: {available_quantity}"
            )

        cursor.execute(
            """
            SELECT unit_price
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if not product:
            raise Exception("Product not found.")

        unit_price = product[0]

        cursor.execute(
            """
            INSERT INTO sales(
                customer_name,
                warehouse_id
            )
            VALUES (%s, %s)
            RETURNING sale_id
            """,
            (customer_name, warehouse_id)
        )

        sale_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO sale_items
            (
                sale_id,
                product_id,
                quantity,
                unit_price
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                sale_id,
                product_id,
                quantity,
                unit_price
            )
        )

        cursor.execute(
            """
            UPDATE inventory
            SET quantity = quantity - %s
            WHERE inventory_id = %s
            """,
            (quantity, inventory_id)
        )

        connection.commit()

        print("Sale completed successfully.")
        print("Sale ID:", sale_id)
        print("Total Amount:", unit_price * quantity)

    except Exception as error:
        connection.rollback()
        print("Transaction failed.")
        print("ROLLBACK executed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()


def create_purchase(
    supplier_id,
    product_id,
    warehouse_id,
    quantity,
    unit_cost
):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO purchases(
                supplier_id,
                warehouse_id
            )
            VALUES (%s, %s)
            RETURNING purchase_id
            """,
            (supplier_id, warehouse_id)
        )

        purchase_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO purchase_items
            (
                purchase_id,
                product_id,
                quantity,
                unit_cost
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                purchase_id,
                product_id,
                quantity,
                unit_cost
            )
        )

        cursor.execute(
            """
            INSERT INTO inventory
            (
                product_id,
                warehouse_id,
                quantity,
                reorder_level
            )
            VALUES (%s, %s, %s, 10)
            ON CONFLICT (product_id, warehouse_id)
            DO UPDATE
            SET quantity =
                inventory.quantity + EXCLUDED.quantity
            """,
            (
                product_id,
                warehouse_id,
                quantity
            )
        )

        connection.commit()

        print("Purchase completed successfully.")
        print("Purchase ID:", purchase_id)
        print("Total Cost:", quantity * unit_cost)

    except Exception as error:
        connection.rollback()
        print("Purchase failed.")
        print("ROLLBACK executed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()


def update_purchase(
    purchase_id,
    supplier_id,
    product_id,
    warehouse_id,
    quantity,
    unit_cost
):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pi.product_id,
                pi.quantity,
                pi.unit_cost,
                p.supplier_id,
                p.warehouse_id
            FROM purchase_items pi
            JOIN purchases p
                ON pi.purchase_id = p.purchase_id
            WHERE pi.purchase_id = %s
            FOR UPDATE
            """,
            (purchase_id,)
        )

        old_data = cursor.fetchone()

        if not old_data:
            raise Exception("Purchase not found.")

        old_product_id = old_data[0]
        old_quantity = old_data[1]
        old_warehouse_id = old_data[4]

        cursor.execute(
            """
            SELECT inventory_id, quantity
            FROM inventory
            WHERE product_id = %s
            AND warehouse_id = %s
            FOR UPDATE
            """,
            (
                old_product_id,
                old_warehouse_id
            )
        )

        old_inventory = cursor.fetchone()

        if not old_inventory:
            raise Exception("Inventory record not found.")

        cursor.execute(
            """
            UPDATE purchases
            SET supplier_id = %s,
                warehouse_id = %s
            WHERE purchase_id = %s
            """,
            (
                supplier_id,
                warehouse_id,
                purchase_id
            )
        )

        cursor.execute(
            """
            UPDATE purchase_items
            SET product_id = %s,
                quantity = %s,
                unit_cost = %s
            WHERE purchase_id = %s
            """,
            (
                product_id,
                quantity,
                unit_cost,
                purchase_id
            )
        )

        cursor.execute(
            """
            UPDATE inventory
            SET quantity = quantity - %s
            WHERE product_id = %s
            AND warehouse_id = %s
            """,
            (
                old_quantity,
                old_product_id,
                old_warehouse_id
            )
        )

        cursor.execute(
            """
            INSERT INTO inventory
            (
                product_id,
                warehouse_id,
                quantity,
                reorder_level
            )
            VALUES (%s, %s, %s, 10)
            ON CONFLICT (product_id, warehouse_id)
            DO UPDATE
            SET quantity =
                inventory.quantity + EXCLUDED.quantity
            """,
            (
                product_id,
                warehouse_id,
                quantity
            )
        )

        connection.commit()

        print("Purchase updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Purchase update failed.")
        print("ROLLBACK executed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()


def delete_purchase(purchase_id):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pi.product_id,
                pi.quantity,
                p.warehouse_id
            FROM purchase_items pi
            JOIN purchases p
                ON pi.purchase_id = p.purchase_id
            WHERE pi.purchase_id = %s
            FOR UPDATE
            """,
            (purchase_id,)
        )

        purchase = cursor.fetchone()

        if not purchase:
            raise Exception("Purchase not found.")

        product_id = purchase[0]
        quantity = purchase[1]
        warehouse_id = purchase[2]

        cursor.execute(
            """
            SELECT quantity
            FROM inventory
            WHERE product_id = %s
            AND warehouse_id = %s
            FOR UPDATE
            """,
            (
                product_id,
                warehouse_id
            )
        )

        inventory = cursor.fetchone()

        if not inventory:
            raise Exception("Inventory record not found.")

        if inventory[0] < quantity:
            raise Exception(
                "Cannot delete purchase because inventory "
                "does not contain enough stock to reverse it."
            )

        cursor.execute(
            """
            UPDATE inventory
            SET quantity = quantity - %s
            WHERE product_id = %s
            AND warehouse_id = %s
            """,
            (
                quantity,
                product_id,
                warehouse_id
            )
        )

        cursor.execute(
            """
            DELETE FROM purchases
            WHERE purchase_id = %s
            """,
            (purchase_id,)
        )

        connection.commit()

        print("Purchase deleted successfully.")
        print("Inventory adjusted successfully.")

    except Exception as error:
        connection.rollback()
        print("Purchase deletion failed.")
        print("ROLLBACK executed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()


def update_sale(
    sale_id,
    customer_name,
    product_id,
    warehouse_id,
    quantity
):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                si.product_id,
                si.quantity,
                s.warehouse_id
            FROM sale_items si
            JOIN sales s
                ON si.sale_id = s.sale_id
            WHERE si.sale_id = %s
            FOR UPDATE
            """,
            (sale_id,)
        )

        old_sale = cursor.fetchone()

        if not old_sale:
            raise Exception("Sale not found.")

        old_product_id = old_sale[0]
        old_quantity = old_sale[1]
        old_warehouse_id = old_sale[2]

        cursor.execute(
            """
            SELECT quantity
            FROM inventory
            WHERE product_id = %s
            AND warehouse_id = %s
            FOR UPDATE
            """,
            (
                product_id,
                warehouse_id
            )
        )

        new_inventory = cursor.fetchone()

        if not new_inventory:
            raise Exception("New inventory record not found.")

        cursor.execute(
            """
            UPDATE inventory
            SET quantity = quantity + %s
            WHERE product_id = %s
            AND warehouse_id = %s
            """,
            (
                old_quantity,
                old_product_id,
                old_warehouse_id
            )
        )

        cursor.execute(
            """
            SELECT quantity
            FROM inventory
            WHERE product_id = %s
            AND warehouse_id = %s
            FOR UPDATE
            """,
            (
                product_id,
                warehouse_id
            )
        )

        current_stock = cursor.fetchone()[0]

        if current_stock < quantity:
            raise Exception(
                f"Insufficient stock. Available: {current_stock}"
            )

        cursor.execute(
            """
            SELECT unit_price
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if not product:
            raise Exception("Product not found.")

        cursor.execute(
            """
            UPDATE sales
            SET customer_name = %s,
                warehouse_id = %s
            WHERE sale_id = %s
            """,
            (
                customer_name,
                warehouse_id,
                sale_id
            )
        )

        cursor.execute(
            """
            UPDATE sale_items
            SET product_id = %s,
                quantity = %s,
                unit_price = %s
            WHERE sale_id = %s
            """,
            (
                product_id,
                quantity,
                product[0],
                sale_id
            )
        )

        cursor.execute(
            """
            UPDATE inventory
            SET quantity = quantity - %s
            WHERE product_id = %s
            AND warehouse_id = %s
            """,
            (
                quantity,
                product_id,
                warehouse_id
            )
        )

        connection.commit()

        print("Sale updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Sale update failed.")
        print("ROLLBACK executed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()


def delete_sale(sale_id):
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                si.product_id,
                si.quantity,
                s.warehouse_id
            FROM sale_items si
            JOIN sales s
                ON si.sale_id = s.sale_id
            WHERE si.sale_id = %s
            FOR UPDATE
            """,
            (sale_id,)
        )

        sale = cursor.fetchone()

        if not sale:
            raise Exception("Sale not found.")

        product_id = sale[0]
        quantity = sale[1]
        warehouse_id = sale[2]

        cursor.execute(
            """
            UPDATE inventory
            SET quantity = quantity + %s
            WHERE product_id = %s
            AND warehouse_id = %s
            """,
            (
                quantity,
                product_id,
                warehouse_id
            )
        )

        cursor.execute(
            """
            DELETE FROM sales
            WHERE sale_id = %s
            """,
            (sale_id,)
        )

        connection.commit()

        print("Sale deleted successfully.")
        print("Inventory restored successfully.")

    except Exception as error:
        connection.rollback()
        print("Sale deletion failed.")
        print("ROLLBACK executed.")
        print("Reason:", error)

    finally:
        cursor.close()
        connection.close()
def view_purchases():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                p.purchase_id,
                s.supplier_name,
                pr.product_name,
                w.warehouse_name,
                pi.quantity,
                pi.unit_cost,
                pi.quantity * pi.unit_cost AS total_cost,
                p.purchase_date
            FROM purchases p
            JOIN suppliers s
                ON p.supplier_id = s.supplier_id
            JOIN purchase_items pi
                ON p.purchase_id = pi.purchase_id
            JOIN products pr
                ON pi.product_id = pr.product_id
            JOIN warehouses w
                ON p.warehouse_id = w.warehouse_id
            ORDER BY p.purchase_id
            """
        )

        rows = cursor.fetchall()

        print("\n========== PURCHASES ==========")

        if not rows:
            print("No purchases found.")

        for row in rows:
            print(
                f"Purchase ID: {row[0]} | "
                f"Supplier: {row[1]} | "
                f"Product: {row[2]} | "
                f"Warehouse: {row[3]} | "
                f"Quantity: {row[4]} | "
                f"Unit Cost: {row[5]} | "
                f"Total: {row[6]} | "
                f"Date: {row[7]}"
            )

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def view_sales():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                s.sale_id,
                s.customer_name,
                p.product_name,
                w.warehouse_name,
                si.quantity,
                si.unit_price,
                si.quantity * si.unit_price AS total_amount,
                s.sale_date
            FROM sales s
            JOIN sale_items si
                ON s.sale_id = si.sale_id
            JOIN products p
                ON si.product_id = p.product_id
            JOIN warehouses w
                ON s.warehouse_id = w.warehouse_id
            ORDER BY s.sale_id
            """
        )

        rows = cursor.fetchall()

        print("\n========== SALES ==========")

        if not rows:
            print("No sales found.")

        for row in rows:
            print(
                f"Sale ID: {row[0]} | "
                f"Customer: {row[1]} | "
                f"Product: {row[2]} | "
                f"Warehouse: {row[3]} | "
                f"Quantity: {row[4]} | "
                f"Unit Price: {row[5]} | "
                f"Total: {row[6]} | "
                f"Date: {row[7]}"
            )

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()