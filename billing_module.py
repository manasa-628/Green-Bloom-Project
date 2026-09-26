
from db_connection import get_connection
from datetime import date


# Create a new bill
def create_bill():
    conn = get_connection()
    cursor = conn.cursor()

    customer_name = input("Enter Customer Name: ")
    plant_name = input("Enter Plant Name: ")
    quantity = int(input("Enter Quantity: "))

    # Check plant availability
    query = """
    SELECT price, quantity
    FROM plants
    WHERE plant_name = %s
    """

    cursor.execute(query, (plant_name,))
    plant = cursor.fetchone()

    if plant is None:
        print("Plant not found!")

        cursor.close()
        conn.close()
        return

    price = plant[0]
    available_quantity = plant[1]

    # Check stock
    if quantity <= 0:
        print("Quantity must be greater than zero!")

    elif quantity > available_quantity:
        print("Insufficient stock!")
        print("Available quantity:", available_quantity)

    else:
        total_amount = price * quantity

        print("\n===== BILL DETAILS =====")
        print("Customer Name:", customer_name)
        print("Plant Name:", plant_name)
        print("Price:", price)
        print("Quantity:", quantity)
        print("Total Amount:", total_amount)

        confirm = input("Confirm purchase? (yes/no): ")

        if confirm.lower() == "yes":

            # Insert sale into sales table
            insert_query = """
            INSERT INTO sales
            (customer_name, plant_name, quantity,
             total_amount, sale_date)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                customer_name,
                plant_name,
                quantity,
                total_amount,
                date.today()
            )

            cursor.execute(insert_query, values)

            # Reduce plant stock
            update_query = """
            UPDATE plants
            SET quantity = quantity - %s
            WHERE plant_name = %s
            """

            cursor.execute(
                update_query,
                (quantity, plant_name)
            )

            conn.commit()

            print("\nPurchase completed successfully!")
            print("Total Amount:", total_amount)

        else:
            print("Purchase cancelled.")

    cursor.close()
    conn.close()


# Billing Menu
if __name__ == "__main__":
    while True:
        print("\n===== BILLING MENU =====")
        print("1. Create Bill")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_bill()

        elif choice == "2":
            print("Exiting Billing Module...")
            break

        else:
            print("Invalid choice!")