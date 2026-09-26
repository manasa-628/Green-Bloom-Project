from db_connection import get_connection


def add_plant():
    try:
        plant_id = int(input("Enter Plant ID: "))
        plant_name = input("Enter Plant Name: ")
        category = input("Enter Category: ")
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        supplier_name = input("Enter Supplier Name: ")

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO plants
        (plant_id, plant_name, category, price, quantity, supplier_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            plant_id,
            plant_name,
            category,
            price,
            quantity,
            supplier_name
        )

        cursor.execute(query, values)
        conn.commit()

        print("Plant added successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def view_plants():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM plants")

        plants = cursor.fetchall()

        print("\n--- Plant Details ---")

        if not plants:
            print("No plants found.")
        else:
            for plant in plants:
                print(plant)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def search_plant():
    try:
        plant_name = input("Enter Plant Name to search: ")

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM plants
        WHERE plant_name LIKE %s
        """

        cursor.execute(query, ("%" + plant_name + "%",))

        plants = cursor.fetchall()

        if not plants:
            print("Plant not found.")
        else:
            print("\n--- Search Results ---")
            for plant in plants:
                print(plant)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def update_plant():
    try:
        plant_id = int(input("Enter Plant ID to update: "))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM plants WHERE plant_id = %s",
            (plant_id,)
        )

        plant = cursor.fetchone()

        if not plant:
            print("Plant not found.")
            cursor.close()
            conn.close()
            return

        print("\nCurrent Plant Details:")
        print(plant)

        plant_name = input(
            f"Enter new Plant Name [{plant[1]}]: "
        ) or plant[1]

        category = input(
            f"Enter new Category [{plant[2]}]: "
        ) or plant[2]

        price_input = input(
            f"Enter new Price [{plant[3]}]: "
        )

        quantity_input = input(
            f"Enter new Quantity [{plant[4]}]: "
        )

        supplier_name = input(
            f"Enter new Supplier Name [{plant[5]}]: "
        ) or plant[5]

        price = float(price_input) if price_input else plant[3]
        quantity = int(quantity_input) if quantity_input else plant[4]

        query = """
        UPDATE plants
        SET plant_name = %s,
            category = %s,
            price = %s,
            quantity = %s,
            supplier_name = %s
        WHERE plant_id = %s
        """

        values = (
            plant_name,
            category,
            price,
            quantity,
            supplier_name,
            plant_id
        )

        cursor.execute(query, values)
        conn.commit()

        print("Plant updated successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def delete_plant():
    try:
        plant_id = int(input("Enter Plant ID to delete: "))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM plants WHERE plant_id = %s",
            (plant_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Plant deleted successfully!")
        else:
            print("Plant not found.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def update_stock():
    try:
        plant_id = int(input("Enter Plant ID: "))
        quantity = int(input("Enter New Quantity: "))

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE plants
        SET quantity = %s
        WHERE plant_id = %s
        """

        cursor.execute(query, (quantity, plant_id))
        conn.commit()

        if cursor.rowcount > 0:
            print("Stock updated successfully!")
        else:
            print("Plant not found.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def plant_management():
    while True:
        print("\n===== PLANT MANAGEMENT =====")
        print("1. Add Plant")
        print("2. View Plants")
        print("3. Search Plant")
        print("4. Update Plant")
        print("5. Delete Plant")
        print("6. Update Stock")
        print("7. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_plant()

        elif choice == "2":
            view_plants()

        elif choice == "3":
            search_plant()

        elif choice == "4":
            update_plant()

        elif choice == "5":
            delete_plant()

        elif choice == "6":
            update_stock()

        elif choice == "7":
            break

        else:
            print("Invalid choice.")