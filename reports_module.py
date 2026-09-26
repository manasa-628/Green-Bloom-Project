
from db_connection import get_connection


# 1. Total Sales Report
def total_sales_report():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT SUM(total_amount)
    FROM sales
    """

    cursor.execute(query)
    result = cursor.fetchone()

    print("\n===== TOTAL SALES REPORT =====")

    if result[0] is not None:
        print("Total Sales Amount:", result[0])
    else:
        print("No sales available.")

    cursor.close()
    conn.close()


# 2. Available Plant Stock
def available_stock():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT plant_id, plant_name, category,
           price, quantity
    FROM plants
    """

    cursor.execute(query)
    plants = cursor.fetchall()

    print("\n===== AVAILABLE PLANT STOCK =====")

    if plants:
        for plant in plants:
            print(plant)
    else:
        print("No plants available.")

    cursor.close()
    conn.close()


# 3. Low Stock Plants
def low_stock_plants():
    conn = get_connection()
    cursor = conn.cursor()

    threshold = 5

    query = """
    SELECT plant_id, plant_name, quantity
    FROM plants
    WHERE quantity <= %s
    """

    cursor.execute(query, (threshold,))
    plants = cursor.fetchall()

    print("\n===== LOW STOCK PLANTS =====")

    if plants:
        for plant in plants:
            print(plant)
    else:
        print("No low stock plants.")

    cursor.close()
    conn.close()


# 4. Customer Purchase History
def customer_purchase_history():
    conn = get_connection()
    cursor = conn.cursor()

    customer_name = input("Enter Customer Name: ")

    query = """
    SELECT sale_id, customer_name, plant_name,
           quantity, total_amount, sale_date
    FROM sales
    WHERE customer_name = %s
    """

    cursor.execute(query, (customer_name,))
    purchases = cursor.fetchall()

    print("\n===== CUSTOMER PURCHASE HISTORY =====")

    if purchases:
        for purchase in purchases:
            print(purchase)
    else:
        print("No purchase history found.")

    cursor.close()
    conn.close()


# Reports Menu
if __name__ == "__main__":
    while True:
        print("\n===== REPORTS MENU =====")
        print("1. Total Sales Report")
        print("2. Available Plant Stock")
        print("3. Low Stock Plants")
        print("4. Customer Purchase History")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            total_sales_report()

        elif choice == "2":
            available_stock()

        elif choice == "3":
            low_stock_plants()

        elif choice == "4":
            customer_purchase_history()

        elif choice == "5":
            print("Exiting Reports Module...")
            break

        else:
            print("Invalid choice!")