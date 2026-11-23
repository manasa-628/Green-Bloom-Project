# 🌱 Green Bloom Nursery Management System

## 📌 Project Description

Green Bloom Nursery Management System is a Python and MySQL-based application developed to manage nursery operations such as plant stock, suppliers, customers, billing, and sales reports.

The project also includes a Streamlit web interface with plant images to provide easy and user-friendly management.

## 🎯 Objectives

- Manage plant stock
- View plant details
- Search plants
- Add new plants
- Update plant details and quantity
- Delete plant records
- Manage supplier information
- Manage customer information
- Generate customer bills
- Automatically update plant stock after a sale
- Generate sales reports

## 🛠️ Technologies Used

- Python
- MySQL
- Streamlit
- MySQL Connector
- Pandas
- VS Code
- Git and GitHub

## 🌿 Features

### Plant Management

- View all plants
- Search plants
- Add new plants
- Update plant details and quantity
- Delete plant records
- View plant price and available stock
- View supplier information
- Display plant images

### Supplier Management

- View supplier details
- Add new suppliers
- Update supplier details
- Delete supplier records
- Manage supplier information

### Customer Management

- View customer details
- Add new customers
- Update customer details
- Delete customer records
- View customer purchase history

### Billing Management

- Select customer
- Select plant
- Enter purchase quantity
- Calculate total amount
- Generate customer bills
- Save sales information
- Update plant stock after a sale

### Sales Reports

- Total Sales Report
- Available Plant Stock Report
- Low Stock Plants Report
- Customer Purchase History
- View sales and transaction details

## 🗄️ Database

**Database Name:**

```text
green_bloom_db
```

### Tables

- plants
- suppliers
- customers
- sales

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
├── .gitignore
└── README.md
```

## ▶️ How to Run the Project

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

### 4. Configure MySQL Database

- Open MySQL Workbench.
- Execute the `database.sql` file to create the required database and tables.
- Configure your MySQL connection details in `db_connection.py`.

### 5. Run the Streamlit Application

```bash
streamlit run app.py
```

The Green Bloom web application will open in your browser.

### 6. Run the Console Application

```bash
python main.py
```

## 🔐 Database Configuration

Open `db_connection.py` and configure your MySQL connection details.

Make sure the database name is:

```text
green_bloom_db
```

**Note:** Do not upload your actual MySQL password to a public GitHub repository.

## 🧪 Testing

The project includes the following functional areas:

- Plant Management
- Plant Search
- Add, Update and Delete Plant Records
- Supplier Management
- Customer Management
- Billing Management
- Stock Updates After Sales
- Sales Reports
- Low Stock Reports
- Plant Image Display
- Streamlit Web Interface

## 👩‍💻 Developer

**Manasa**

B.Tech - Data Science

## 📌 Conclusion

The Green Bloom Nursery Management System provides a simple and efficient solution for managing nursery operations, including plant inventory, suppliers, customers, billing, and sales reports.

The project combines Python, MySQL, and Streamlit to provide database management along with a user-friendly web interface.
