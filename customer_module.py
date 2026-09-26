
from db_connection import get_connection


# 1. Add a new customer
def add_customer():
    conn = get_connection()
    cursor = conn.cursor()

    customer_id = int(input("Enter Customer ID: "))
    customer_name = input("Enter Customer Name: ")
    phone = input("Enter Phone Number: ")
    city = input("Enter City: ")

    query = """
    INSERT INTO customers
    (customer_id, customer_name, phone, city)
    VALUES (%s, %s, %s, %s)
    """

    values = (customer_id, customer_name, phone, city)

    cursor.execute(query, values)
    conn.commit()

    print("Customer added successfully!")

    cursor.close()
    conn.close()


# 2. View all customers
def view_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    print("\n===== CUSTOMER DETAILS =====")

    if customers:
        for customer in customers:
            print(customer)
    else:
        print("No customers found.")

    cursor.close()
    conn.close()


# 3. View customer purchase history
def customer_history():
    conn = get_connection()
    cursor = conn.cursor()

    customer_name = input("Enter Customer Name: ")

    query = """
    SELECT * FROM sales
    WHERE customer_name = %s
    """

    cursor.execute(query, (customer_name,))

    history = cursor.fetchall()

    print("\n===== CUSTOMER PURCHASE HISTORY =====")

    if history:
        for sale in history:
            print(sale)
    else:
        print("No purchase history found.")

    cursor.close()
    conn.close()


# 4. Track customer purchases
def track_purchases():
    conn = get_connection()
    cursor = conn.cursor()

    customer_name = input("Enter Customer Name: ")

    query = """
    SELECT customer_name,
           SUM(total_amount) AS total_purchase
    FROM sales
    WHERE customer_name = %s
    GROUP BY customer_name
    """

    cursor.execute(query, (customer_name,))

    result = cursor.fetchone()

    if result:
        print("\n===== CUSTOMER PURCHASE SUMMARY =====")
        print("Customer Name:", result[0])
        print("Total Purchase Amount:", result[1])
    else:
        print("No purchases found for this customer.")

    cursor.close()
    conn.close()


# 5. Customer Menu
if __name__ == "__main__":
    while True:
        print("\n===== CUSTOMER MENU =====")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Customer Purchase History")
        print("4. Track Customer Purchases")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_customer()

        elif choice == "2":
            view_customers()

        elif choice == "3":
            customer_history()

        elif choice == "4":
            track_purchases()

        elif choice == "5":
            print("Exiting Customer Module...")
            break

        else:
            print("Invalid choice!")