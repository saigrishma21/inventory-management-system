from app.db import get_connection


def add_category(name, description):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO categories(category_name, description)
            VALUES (%s, %s)
            RETURNING category_id
            """,
            (name, description)
        )

        category_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Category added successfully. ID: {category_id}")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def get_categories():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT category_id, category_name, description
        FROM categories
        ORDER BY category_id
        """
    )

    rows = cursor.fetchall()

    print("\n--- Categories ---")

    for row in rows:
        print(row)

    cursor.close()
    connection.close()


def update_category(category_id, name, description):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE categories
            SET category_name = %s,
                description = %s
            WHERE category_id = %s
            """,
            (name, description, category_id)
        )

        connection.commit()
        print("Category updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def delete_category(category_id):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM categories
            WHERE category_id = %s
            """,
            (category_id,)
        )

        connection.commit()
        print("Category deleted successfully.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()