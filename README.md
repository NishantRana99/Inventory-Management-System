# Inventory-Management-System
An interactive Inventory Management System built using MySQL, Python, Pandas, and Streamlit. The project provides a simple interface for monitoring inventory information and performing common inventory operations such as adding products, checking product history, placing reorders, and receiving reorders.



##  Project Overview

The goal of this project is to build a centralized inventory management application where inventory and supplier information is stored in a **MySQL database** and managed through a **Python + Streamlit** application.

The project combines SQL database operations with a user-friendly interface to perform both reporting and operational inventory tasks.

###  Project Workflow

```text
User
 ↓
Streamlit Application
 ↓
Python Database Functions
 ↓
MySQL Database
 ↓
SQL Queries / Views / Stored Procedures
 ↓
Results
 ↓
Streamlit Dashboard
```

## Technologies Used

* **Python** – Application logic and database connectivity
* **MySQL** – Database management and SQL operations
* **Streamlit** – Interactive web application
* **Pandas** – Data handling and tabular data display
* **mysql-connector-python** – Python-MySQL connectivity

##  Features

### Basic Information Dashboard

The dashboard displays important inventory and supply-chain metrics:

* Total Suppliers
* Total Products
* Total Categories
* Total Sale Value (Last 3 Months)
* Total Restock Value (Last 3 Months)
* Products Below Reorder Level

It also displays detailed tables for:

* Supplier Contact Details
* Products with Supplier and Stock
* Products Needing Reorder

## Add New Product

Users can add a new product through a Streamlit form.

The form collects:

* Product Name
* Category
* Price
* Stock Quantity
* Reorder Level
* Supplier

The application validates the product name and calls a MySQL stored procedure to add the product.

##  Product History

Users can select a product and view its inventory history.

The application retrieves the selected product's history from the `product_inventory_history` view and displays the records in a table.

##  Place Reorder

Users can:

1. Select a product
2. Enter the reorder quantity
3. Place the reorder

The reorder information is inserted into the MySQL `reorders` table.

##  Receive Reorder

Users can select a reorder and mark it as received.

The application calls a MySQL stored procedure to process the receiving operation.

##  Database Structure

The project uses the following main tables:

```text
products
suppliers
reorders
shipments
stock_entries
```

### Database View

```text
product_inventory_history
```

The view is used to retrieve the inventory history of a selected product.

##  SQL Concepts Used

This project demonstrates several SQL concepts:

* `SELECT`
* `WHERE`
* `JOIN`
* `COUNT()`
* `COUNT(DISTINCT ...)`
* `SUM()`
* `ROUND()`
* `ABS()`
* `MAX()`
* `DATE_SUB()`
* Subqueries
* `ORDER BY`
* `UNION ALL`
* Views
* Stored Procedures
* Transactions
* Parameterised Queries

### Example: Finding Products That Need Reordering

```sql
SELECT product_name, stock_quantity, reorder_level
FROM products
WHERE stock_quantity <= reorder_level;
```

This query identifies products where the current stock is at or below the defined reorder level.

## Python Implementation

The Python code is divided into two main files.

### `app.py`

The Streamlit application handles:

* User interface
* Dashboard metrics
* Forms
* Product selection
* Reorder operations
* Displaying database results

### `db_function.py`

The database module handles:

* MySQL connection
* SQL queries
* Retrieving products and suppliers
* Product history
* Adding products
* Placing reorders
* Receiving reorders
* Calling stored procedures

This separation keeps the UI and database operations organized.

##  Project Structure

```text
Inventory-Management-System/
│
├── app.py
├── db_function.py
├── 1.sql
│
├── products.csv
├── suppliers.csv
├── reorders.csv
├── shipments.csv
├── stock_entries.csv
│
├── screenshots/
│   └── dashboard.png
│
├── requirements.txt
└── README.md
```
