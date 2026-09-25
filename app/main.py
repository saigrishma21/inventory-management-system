from app.categories import (
    add_category,
    get_categories,
    update_category,
    delete_category
)

from app.suppliers import (
    add_supplier,
    get_suppliers,
    update_supplier,
    delete_supplier
)

from app.products import (
    add_product,
    get_products,
    update_product,
    delete_product
)

from app.warehouses import (
    add_warehouse,
    get_warehouses,
    update_warehouse,
    delete_warehouse
)
from app.inventory import (
    add_inventory,
    get_inventory,
    update_inventory,
    delete_inventory
)


from app.transactions import (
    create_sale,
    create_purchase,
    update_purchase,
    delete_purchase,
    update_sale,
    delete_sale,
    view_purchases,
    view_sales
)

from app.reports import (
    inventory_report,
    low_stock_report,
    sales_report,
    supplier_purchase_report,
    total_sales_report
)


def category_menu():
    while True:
        print("\n========== CATEGORY MENU ==========")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Category name: ")
            description = input("Description: ")
            add_category(name, description)

        elif choice == "2":
            get_categories()

        elif choice == "3":
            category_id = int(input("Category ID: "))
            name = input("New category name: ")
            description = input("New description: ")
            update_category(
                category_id,
                name,
                description
            )

        elif choice == "4":
            category_id = int(input("Category ID: "))
            delete_category(category_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def supplier_menu():
    while True:
        print("\n========== SUPPLIER MENU ==========")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Supplier name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            address = input("Address: ")

            add_supplier(
                name,
                email,
                phone,
                address
            )

        elif choice == "2":
            get_suppliers()

        elif choice == "3":
            supplier_id = int(
                input("Supplier ID: ")
            )

            name = input("Supplier name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            address = input("Address: ")

            update_supplier(
                supplier_id,
                name,
                email,
                phone,
                address
            )

        elif choice == "4":
            supplier_id = int(
                input("Supplier ID: ")
            )

            delete_supplier(supplier_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def product_menu():
    while True:
        print("\n========== PRODUCT MENU ==========")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Product name: ")
            category_id = int(
                input("Category ID: ")
            )
            sku = input("SKU: ")
            price = float(
                input("Unit price: ")
            )

            add_product(
                name,
                category_id,
                sku,
                price
            )

        elif choice == "2":
            get_products()

        elif choice == "3":
            product_id = int(
                input("Product ID: ")
            )

            name = input("Product name: ")
            category_id = int(
                input("Category ID: ")
            )
            sku = input("SKU: ")
            price = float(
                input("Unit price: ")
            )

            update_product(
                product_id,
                name,
                category_id,
                sku,
                price
            )

        elif choice == "4":
            product_id = int(
                input("Product ID: ")
            )

            delete_product(product_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def warehouse_menu():
    while True:
        print("\n========== WAREHOUSE MENU ==========")
        print("1. Add Warehouse")
        print("2. View Warehouses")
        print("3. Update Warehouse")
        print("4. Delete Warehouse")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Warehouse name: ")
            location = input("Location: ")

            add_warehouse(
                name,
                location
            )

        elif choice == "2":
            get_warehouses()

        elif choice == "3":
            warehouse_id = int(
                input("Warehouse ID: ")
            )

            name = input("New warehouse name: ")
            location = input("New location: ")

            update_warehouse(
                warehouse_id,
                name,
                location
            )

        elif choice == "4":
            warehouse_id = int(
                input("Warehouse ID: ")
            )

            delete_warehouse(warehouse_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def inventory_menu():
    while True:
        print("\n========== INVENTORY MENU ==========")
        print("1. Add Inventory")
        print("2. View Inventory")
        print("3. Update Inventory")
        print("4. Delete Inventory")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            product_id = int(
                input("Product ID: ")
            )

            warehouse_id = int(
                input("Warehouse ID: ")
            )

            quantity = int(
                input("Quantity: ")
            )

            reorder = int(
                input("Reorder level: ")
            )

            add_inventory(
                product_id,
                warehouse_id,
                quantity,
                reorder
            )

        elif choice == "2":
            get_inventory()

        elif choice == "3":
            inventory_id = int(
                input("Inventory ID: ")
            )

            quantity = int(
                input("New quantity: ")
            )

            reorder = int(
                input("New reorder level: ")
            )

            update_inventory(
                inventory_id,
                quantity,
                reorder
            )

        elif choice == "4":
            inventory_id = int(
                input("Inventory ID: ")
            )

            delete_inventory(inventory_id)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def transaction_menu():
    while True:
        print("\n========== TRANSACTION MENU ==========")
        print("1. Create Purchase")
        print("2. Create Sale")
        print("3. View Purchases")
        print("4. View Sales")
        print("5. Update Purchase")
        print("6. Delete Purchase")
        print("7. Update Sale")
        print("8. Delete Sale")
        print("9. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            supplier_id = int(input("Supplier ID: "))
            product_id = int(input("Product ID: "))
            warehouse_id = int(input("Warehouse ID: "))
            quantity = int(input("Quantity: "))
            unit_cost = float(input("Unit cost: "))

            create_purchase(
                supplier_id,
                product_id,
                warehouse_id,
                quantity,
                unit_cost
            )

        elif choice == "2":
            customer_name = input("Customer name: ")
            product_id = int(input("Product ID: "))
            warehouse_id = int(input("Warehouse ID: "))
            quantity = int(input("Quantity: "))

            create_sale(
                customer_name,
                product_id,
                warehouse_id,
                quantity
            )

        elif choice == "3":
            view_purchases()

        elif choice == "4":
            view_sales()

        elif choice == "5":
            purchase_id = int(input("Purchase ID: "))
            supplier_id = int(input("Supplier ID: "))
            product_id = int(input("Product ID: "))
            warehouse_id = int(input("Warehouse ID: "))
            quantity = int(input("Quantity: "))
            unit_cost = float(input("Unit cost: "))

            update_purchase(
                purchase_id,
                supplier_id,
                product_id,
                warehouse_id,
                quantity,
                unit_cost
            )

        elif choice == "6":
            purchase_id = int(input("Purchase ID: "))

            confirm = input(
                "Delete this purchase? (yes/no): "
            )

            if confirm.lower() == "yes":
                delete_purchase(purchase_id)

        elif choice == "7":
            sale_id = int(input("Sale ID: "))
            customer_name = input("Customer name: ")
            product_id = int(input("Product ID: "))
            warehouse_id = int(input("Warehouse ID: "))
            quantity = int(input("Quantity: "))

            update_sale(
                sale_id,
                customer_name,
                product_id,
                warehouse_id,
                quantity
            )

        elif choice == "8":
            sale_id = int(input("Sale ID: "))

            confirm = input(
                "Delete this sale? (yes/no): "
            )

            if confirm.lower() == "yes":
                delete_sale(sale_id)

        elif choice == "9":
            break

        else:
            print("Invalid choice.")

def report_menu():
    while True:
        print("\n========== REPORT MENU ==========")
        print("1. Inventory Report")
        print("2. Low Stock Report")
        print("3. Sales Report")
        print("4. Supplier Purchase Report")
        print("5. Business Summary")
        print("6. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            inventory_report()

        elif choice == "2":
            low_stock_report()

        elif choice == "3":
            sales_report()

        elif choice == "4":
            supplier_purchase_report()

        elif choice == "5":
            total_sales_report()

        elif choice == "6":
            break

        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n======================================")
        print(" INVENTORY MANAGEMENT SYSTEM")
        print("======================================")

        print("1. Category Management")
        print("2. Supplier Management")
        print("3. Product Management")
        print("4. Warehouse Management")
        print("5. Inventory Management")
        print("6. Transactions")
        print("7. Reports")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            category_menu()

        elif choice == "2":
            supplier_menu()

        elif choice == "3":
            product_menu()

        elif choice == "4":
            warehouse_menu()

        elif choice == "5":
            inventory_menu()

        elif choice == "6":
            transaction_menu()

        elif choice == "7":
            report_menu()

        elif choice == "8":
            print("Application closed.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()