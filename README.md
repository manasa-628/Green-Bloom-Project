# 🌱 Green Bloom Nursery Management System

A **Nursery Management System** developed using **Python, Streamlit, and MySQL** to manage plants, suppliers, customers, billing, inventory, and reports.

## 📌 Project Overview

Green Bloom Nursery Management System provides a simple interface for managing nursery operations. It allows users to maintain plant information, supplier and customer details, process customer purchases, and generate useful reports.

## ✨ Features

* 🌱 Plant Management
* 🚚 Supplier Management
* 👤 Customer Management
* 🧾 Billing Management
* 📊 Sales Reports
* 📦 Plant Stock Management
* ⚠️ Low Stock Reports
* 🖼️ Plant Image Upload
* 🔎 Plant Search

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **MySQL**
* **MySQL Connector**
* **Pandas**
* **Git & GitHub**

## 📂 Project Structure

```text
Green-Bloom-Project/
│
├── Images/
│   ├── Aloe vera.jpg
│   ├── Jasmine.jpg
│   ├── Money Plant.jpg
│   ├── Tulips.jpg
│   ├── Tulsi.jpg
│   ├── rose.jpg
│   └── sunflower.jpg
│
├── app.py
├── main.py
├── plant_module.py
├── supplier_module.py
├── customer_module.py
├── billing_module.py
├── reports_module.py
├── db_connection.py
├── database.sql
├── requirements.txt
└── .gitignore
```

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/manasa-628/Green-Bloom-Project.git
```

### 2. Open the project folder

```bash
cd Green-Bloom-Project
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create the required database using:

```text
database.sql
```

Update the MySQL connection details in `db_connection.py` according to your local MySQL setup.

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

## 📊 Main Modules

### Plant Management

Add, update, search, and manage plant information including plant images, price, quantity, category, and supplier.

### Supplier Management

Manage supplier information.

### Customer Management

Store and manage customer details.

### Billing Management

Create customer bills and automatically update available plant stock.

### Reports Management

Generate reports such as:

* Total Sales Report
* Available Plant Stock
* Low Stock Plants
* Customer Purchase History

## 👩‍💻 Author

**Manasa**

GitHub: **manasa-628**
