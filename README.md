# Inventory Management System

A Python and PostgreSQL-based Inventory Management System designed to manage products, suppliers, warehouses, inventory, purchases, sales, and business reports.

The project demonstrates practical implementation of database normalization, CRUD operations, SQL joins, transactions, foreign-key relationships, inventory tracking, reporting, and Python-PostgreSQL connectivity.

---

## Features

### Category Management

- Add Category
- View Categories
- Update Category
- Delete Category

### Supplier Management

- Add Supplier
- View Suppliers
- Update Supplier
- Delete Supplier
- Prevent deletion of suppliers used in purchase records

### Product Management

- Add Product
- View Products
- Update Product
- Delete Product
- Maintain product SKU
- Associate products with categories
- Prevent deletion of products used by inventory, purchases, or sales

### Warehouse Management

- Add Warehouse
- View Warehouses
- Update Warehouse
- Delete Warehouse
- Track inventory by warehouse
- Prevent deletion of warehouses used by existing records

### Inventory Management

- Add Inventory
- View Inventory
- Update Inventory
- Delete Inventory
- Track product quantities
- Maintain reorder levels
- Track inventory for different warehouses

### Transaction Management

- Create Purchase
- View Purchases
- Update Purchase
- Delete Purchase
- Create Sale
- View Sales
- Update Sale
- Delete Sale
- Automatically increase inventory after purchases
- Automatically decrease inventory after sales
- Restore inventory when sales are deleted
- Reverse inventory changes when purchases are deleted
- Use database transactions with COMMIT and ROLLBACK
- Prevent sales when sufficient stock is unavailable

### Reports

- Inventory Report
- Low Stock Report
- Sales Report
- Supplier Purchase Report
- Business Summary

---

## Technologies Used

- Python
- PostgreSQL
- SQL
- psycopg2
- python-dotenv
- Git
- GitHub

---

## Project Structure

```text
inventory-management-system/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── categories.py
│   ├── suppliers.py
│   ├── products.py
│   ├── warehouses.py
│   ├── inventory.py
│   ├── transactions.py
│   ├── reports.py
│   └── main.py
│
├── database/
│   └── schema.sql
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
