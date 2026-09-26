
from db_connection import get_connection

# add a new supplier to the database
def add_supplier():
    conn = get_connection()
    cursor = conn.cursor()

    supplier_id = input("Enter Supplier ID: ")
    supplier_name = input("Enter Supplier Name: ")
    phone = input("Enter Phone Number: ")
    city = input("Enter City: ")

    query = """
    INSERT INTO suppliers
    (supplier_id, supplier_name, phone, city)
    VALUES (%s, %s, %s, %s)
    """

    values = (supplier_id, supplier_name, phone, city)

    cursor.execute(query, values)
    conn.commit()

    print("Supplier added successfully!")

    cursor.close()
    conn.close()

    
    
# view all suppliers

def view_suppliers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM suppliers")

    suppliers = cursor.fetchall()

    print("\n===== SUPPLIER DETAILS =====")

    if suppliers:
        for supplier in suppliers:
            print(supplier)
    else:
        print("No suppliers found.")

    cursor.close()
    conn.close()

    

# update supplier details

def update_supplier():
    conn = get_connection()
    cursor = conn.cursor()

    supplier_id = input("Enter Supplier ID to update: ")

    new_name = input("Enter New Supplier Name: ")
    new_phone = input("Enter New Phone Number: ")
    new_city = input("Enter New City: ")

    query = """
    UPDATE suppliers
    SET supplier_name = %s,
        phone = %s,
        city = %s
    WHERE supplier_id = %s
    """

    values = (new_name, new_phone, new_city, supplier_id)

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount > 0:
        print("Supplier details updated successfully!")
    else:
        print("Supplier ID not found.")

    cursor.close()
    conn.close()
    

    

# delete a supplier
def delete_supplier():
    conn = get_connection()
    cursor = conn.cursor()

    supplier_id = input("Enter Supplier ID to delete: ")

    query = """
    DELETE FROM suppliers
    WHERE supplier_id = %s
    """

    cursor.execute(query, (supplier_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Supplier deleted successfully!")
    else:
        print("Supplier ID not found.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    while True:
        print("\n===== SUPPLIER MENU =====")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_supplier()

        elif choice == "2":
            view_suppliers()

        elif choice == "3":
            update_supplier()

        elif choice == "4":
            delete_supplier()

        elif choice == "5":
            print("Exiting Supplier Module...")
            break

        else:
            print("Invalid choice!")