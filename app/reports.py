from app.db import get_connection


def inventory_report():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            p.product_name,
            p.sku,
            c.category_name,
            w.warehouse_name,
            i.quantity,
            i.reorder_level,
            p.unit_price,
            i.quantity * p.unit_price AS inventory_value
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN categories c
            ON p.category_id = c.category_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        ORDER BY inventory_value DESC
        """
    )

    rows = cursor.fetchall()

    print("\n========== INVENTORY REPORT ==========")

    for row in rows:
        print(
            f"Product: {row[0]} | "
            f"SKU: {row[1]} | "
            f"Category: {row[2]} | "
            f"Warehouse: {row[3]} | "
            f"Stock: {row[4]} | "
            f"Reorder: {row[5]} | "
            f"Price: {row[6]} | "
            f"Value: {row[7]}"
        )

    cursor.close()
    connection.close()


def low_stock_report():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
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
        WHERE i.quantity <= i.reorder_level
        ORDER BY i.quantity ASC
        """
    )

    rows = cursor.fetchall()

    print("\n========== LOW STOCK REPORT ==========")

    if not rows:
        print("No low-stock products.")

    for row in rows:
        print(
            f"Product: {row[0]} | "
            f"SKU: {row[1]} | "
            f"Warehouse: {row[2]} | "
            f"Stock: {row[3]} | "
            f"Reorder Level: {row[4]}"
        )

    cursor.close()
    connection.close()


def sales_report():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            p.product_name,
            SUM(si.quantity) AS units_sold,
            SUM(si.quantity * si.unit_price) AS revenue
        FROM sale_items si
        JOIN products p
            ON si.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        """
    )

    rows = cursor.fetchall()

    print("\n========== SALES REPORT ==========")

    for row in rows:
        print(
            f"Product: {row[0]} | "
            f"Units Sold: {row[1]} | "
            f"Revenue: {row[2]}"
        )

    cursor.close()
    connection.close()


def supplier_purchase_report():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            s.supplier_name,
            COUNT(DISTINCT p.purchase_id) AS purchase_count,
            SUM(pi.quantity * pi.unit_cost) AS total_purchase_value
        FROM suppliers s
        JOIN purchases p
            ON s.supplier_id = p.supplier_id
        JOIN purchase_items pi
            ON p.purchase_id = pi.purchase_id
        GROUP BY s.supplier_id, s.supplier_name
        ORDER BY total_purchase_value DESC
        """
    )

    rows = cursor.fetchall()

    print("\n========== SUPPLIER PURCHASE REPORT ==========")

    for row in rows:
        print(
            f"Supplier: {row[0]} | "
            f"Purchases: {row[1]} | "
            f"Purchase Value: {row[2]}"
        )

    cursor.close()
    connection.close()


def total_sales_report():
    connection = get_connection()

    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(DISTINCT s.sale_id) AS total_orders,
            COALESCE(
                SUM(si.quantity * si.unit_price),
                0
            ) AS total_revenue
        FROM sales s
        LEFT JOIN sale_items si
            ON s.sale_id = si.sale_id
        """
    )

    row = cursor.fetchone()

    print("\n========== BUSINESS SUMMARY ==========")
    print("Total Orders:", row[0])
    print("Total Revenue:", row[1])

    cursor.close()
    connection.close()