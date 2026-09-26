import streamlit as st
import pandas as pd
import mysql.connector
from datetime import date


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Green Bloom Plants",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Green Bloom Plants")
st.write("Plant Stack Management System")


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="green_bloom_db"
    )


# =========================================================
# PLANT IMAGE MAPPING
# =========================================================

plant_images = {
    "Tulsi": "images/tulsi.jpg",
    "Aloe Vera": "images/aloe_vera.jpg",
    "Money Plant": "images/money_plant.jpg",
    "Jasmine": "images/jasmine.jpg",
    "Rose": "images/rose.jpg",
    "rose": "images/rose.jpg",
    "Tulips": "images/tulips.jpg"
}


# =========================================================
# FETCH DATA FROM DATABASE
# =========================================================

def fetch_dataframe(query, params=None):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params or ())

        rows = cursor.fetchall()

        if cursor.description:
            columns = [column[0] for column in cursor.description]
        else:
            columns = []

        return pd.DataFrame(rows, columns=columns)

    except Exception as e:

        st.error(f"Database error: {e}")

        return pd.DataFrame()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# EXECUTE INSERT / UPDATE / DELETE
# =========================================================

def execute_query(query, params=(), success_message=None):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params)

        connection.commit()

        if success_message:
            st.success(success_message)

        return True

    except Exception as e:

        if connection:
            connection.rollback()

        st.error(f"Database error: {e}")

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# PLANT MANAGEMENT
# =========================================================

def plant_management():

    st.header("🌿 Plant Management")

    option = st.selectbox(
        "Choose an operation",
        [
            "View Plants",
            "Add Plant",
            "Update Plant",
            "Delete Plant",
            "Search Plant"
        ]
    )


    # -----------------------------------------------------
    # VIEW PLANTS
    # -----------------------------------------------------

    if option == "View Plants":

        st.subheader("🌱 Available Plants")

        df = fetch_dataframe(
            """
            SELECT plant_id,
                   plant_name,
                   category,
                   price,
                   quantity,
                   supplier_name
            FROM plants
            ORDER BY plant_id
            """
        )

        if df.empty:

            st.info("No plants found.")

            return


        # Display plants in cards

        for start in range(0, len(df), 3):

            cols = st.columns(3)

            for i, col in enumerate(cols):

                index = start + i

                if index >= len(df):
                    break

                row = df.iloc[index]

                with col:

                    st.markdown("---")

                    plant_name = str(row["plant_name"])

                    image_path = plant_images.get(plant_name)


                    # Display image

                    if image_path:

                        try:

                            st.image(
                                image_path,
                                caption=plant_name,
                                width=220
                            )

                        except Exception:

                            st.info("🌱 Image not found")

                    else:

                        st.info("🌱 No image added")


                    st.markdown(f"### {plant_name}")

                    st.write(
                        f"**Plant ID:** {row['plant_id']}"
                    )

                    st.write(
                        f"**Category:** {row['category']}"
                    )

                    st.write(
                        f"**Price:** ₹{row['price']}"
                    )

                    st.write(
                        f"**Stock:** {row['quantity']}"
                    )

                    st.write(
                        f"**Supplier:** {row['supplier_name']}"
                    )


        # Display table

        st.markdown("---")

        st.subheader("📋 Plant Table")

        st.dataframe(
            df,
            use_container_width=True
        )


    # -----------------------------------------------------
    # ADD PLANT
    # -----------------------------------------------------

    elif option == "Add Plant":

        st.subheader("➕ Add New Plant")

        with st.form("add_plant_form"):

            plant_id = st.number_input(
                "Plant ID",
                min_value=1,
                step=1
            )

            plant_name = st.text_input(
                "Plant Name"
            )

            category = st.text_input(
                "Category"
            )

            price = st.number_input(
                "Price",
                min_value=0.0,
                step=10.0
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                step=1
            )

            supplier_name = st.text_input(
                "Supplier Name"
            )

            submitted = st.form_submit_button(
                "Add Plant"
            )


        if submitted:

            if not plant_name.strip():

                st.warning(
                    "Please enter plant name."
                )

            elif not category.strip():

                st.warning(
                    "Please enter category."
                )

            else:

                execute_query(
                    """
                    INSERT INTO plants
                    (
                        plant_id,
                        plant_name,
                        category,
                        price,
                        quantity,
                        supplier_name
                    )
                    VALUES
                    (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        plant_id,
                        plant_name,
                        category,
                        price,
                        quantity,
                        supplier_name
                    ),
                    "Plant added successfully! 🌱"
                )


    # -----------------------------------------------------
    # UPDATE PLANT
    # -----------------------------------------------------

    elif option == "Update Plant":

        st.subheader("✏️ Update Plant")

        df = fetch_dataframe(
            """
            SELECT
                plant_id,
                plant_name,
                price,
                quantity
            FROM plants
            ORDER BY plant_id
            """
        )

        if df.empty:

            st.info("No plants available.")

            return


        plant_id = st.selectbox(
            "Select Plant ID",
            df["plant_id"].tolist()
        )


        selected = df[
            df["plant_id"] == plant_id
        ].iloc[0]


        new_name = st.text_input(
            "Plant Name",
            value=str(selected["plant_name"])
        )


        new_price = st.number_input(
            "Price",
            min_value=0.0,
            value=float(selected["price"]),
            step=10.0
        )


        new_quantity = st.number_input(
            "Quantity",
            min_value=0,
            value=int(selected["quantity"]),
            step=1
        )


        if st.button("Update Plant"):

            execute_query(
                """
                UPDATE plants
                SET plant_name=%s,
                    price=%s,
                    quantity=%s
                WHERE plant_id=%s
                """,
                (
                    new_name,
                    new_price,
                    new_quantity,
                    plant_id
                ),
                "Plant updated successfully! ✅"
            )


    # -----------------------------------------------------
    # DELETE PLANT
    # -----------------------------------------------------

    elif option == "Delete Plant":

        st.subheader("🗑️ Delete Plant")

        df = fetch_dataframe(
            """
            SELECT plant_id,
                   plant_name
            FROM plants
            ORDER BY plant_id
            """
        )

        if df.empty:

            st.info("No plants available.")

            return


        plant_id = st.selectbox(
            "Select Plant",
            df["plant_id"].tolist()
        )


        name = df[
            df["plant_id"] == plant_id
        ]["plant_name"].iloc[0]


        st.warning(
            f"You selected: {name}"
        )


        if st.button("Delete Plant"):

            execute_query(
                """
                DELETE FROM plants
                WHERE plant_id=%s
                """,
                (plant_id,),
                "Plant deleted successfully."
            )


    # -----------------------------------------------------
    # SEARCH PLANT
    # -----------------------------------------------------

    elif option == "Search Plant":

        st.subheader("🔎 Search Plant")

        search_name = st.text_input(
            "Enter plant name"
        )


        if search_name:

            df = fetch_dataframe(
                """
                SELECT *
                FROM plants
                WHERE plant_name LIKE %s
                """,
                (f"%{search_name}%",)
            )


            if df.empty:

                st.warning(
                    "No plant found."
                )

            else:

                st.dataframe(
                    df,
                    use_container_width=True
                )


# =========================================================
# SUPPLIER MANAGEMENT
# =========================================================

def supplier_management():

    st.header("🚚 Supplier Management")

    option = st.selectbox(
        "Choose an operation",
        [
            "View Suppliers",
            "Add Supplier",
            "Update Supplier",
            "Delete Supplier"
        ]
    )


    # -----------------------------------------------------
    # VIEW SUPPLIERS
    # -----------------------------------------------------

    if option == "View Suppliers":

        df = fetch_dataframe(
            """
            SELECT *
            FROM suppliers
            ORDER BY supplier_id
            """
        )


        if df.empty:

            st.info(
                "No suppliers found."
            )

        else:

            st.dataframe(
                df,
                use_container_width=True
            )


    # -----------------------------------------------------
    # ADD SUPPLIER
    # -----------------------------------------------------

    elif option == "Add Supplier":

        st.subheader("➕ Add Supplier")

        with st.form("add_supplier_form"):

            supplier_id = st.text_input(
                "Supplier ID"
            )

            supplier_name = st.text_input(
                "Supplier Name"
            )

            phone = st.text_input(
                "Phone"
            )

            city = st.text_input(
                "City"
            )

            submitted = st.form_submit_button(
                "Add Supplier"
            )


        if submitted:

            execute_query(
                """
                INSERT INTO suppliers
                (
                    supplier_id,
                    supplier_name,
                    phone,
                    city
                )
                VALUES
                (%s, %s, %s, %s)
                """,
                (
                    supplier_id,
                    supplier_name,
                    phone,
                    city
                ),
                "Supplier added successfully! ✅"
            )


    # -----------------------------------------------------
    # UPDATE SUPPLIER
    # -----------------------------------------------------

    elif option == "Update Supplier":

        st.subheader("✏️ Update Supplier")

        df = fetch_dataframe(
            """
            SELECT *
            FROM suppliers
            ORDER BY supplier_id
            """
        )


        if df.empty:

            st.info(
                "No suppliers found."
            )

            return


        supplier_id = st.selectbox(
            "Select Supplier ID",
            df["supplier_id"].tolist()
        )


        selected = df[
            df["supplier_id"] == supplier_id
        ].iloc[0]


        supplier_name = st.text_input(
            "Supplier Name",
            value=str(
                selected["supplier_name"]
            )
        )


        phone = st.text_input(
            "Phone",
            value=str(selected["phone"])
        )


        city = st.text_input(
            "City",
            value=str(selected["city"])
        )


        if st.button("Update Supplier"):

            execute_query(
                """
                UPDATE suppliers
                SET supplier_name=%s,
                    phone=%s,
                    city=%s
                WHERE supplier_id=%s
                """,
                (
                    supplier_name,
                    phone,
                    city,
                    supplier_id
                ),
                "Supplier updated successfully! ✅"
            )


    # -----------------------------------------------------
    # DELETE SUPPLIER
    # -----------------------------------------------------

    elif option == "Delete Supplier":

        st.subheader("🗑️ Delete Supplier")

        df = fetch_dataframe(
            """
            SELECT supplier_id,
                   supplier_name
            FROM suppliers
            """
        )


        if df.empty:

            st.info(
                "No suppliers found."
            )

            return


        supplier_id = st.selectbox(
            "Select Supplier",
            df["supplier_id"].tolist()
        )


        if st.button("Delete Supplier"):

            execute_query(
                """
                DELETE FROM suppliers
                WHERE supplier_id=%s
                """,
                (supplier_id,),
                "Supplier deleted successfully."
            )


# =========================================================
# CUSTOMER MANAGEMENT
# =========================================================

def customer_management():

    st.header("👤 Customer Management")

    option = st.selectbox(
        "Choose an operation",
        [
            "View Customers",
            "Add Customer",
            "Customer Purchase History",
            "Track Customer Purchases"
        ]
    )


    # -----------------------------------------------------
    # VIEW CUSTOMERS
    # -----------------------------------------------------

    if option == "View Customers":

        df = fetch_dataframe(
            """
            SELECT *
            FROM customers
            ORDER BY customer_id
            """
        )


        if df.empty:

            st.info(
                "No customers found."
            )

        else:

            st.dataframe(
                df,
                use_container_width=True
            )


    # -----------------------------------------------------
    # ADD CUSTOMER
    # -----------------------------------------------------

    elif option == "Add Customer":

        st.subheader("➕ Add Customer")

        with st.form("add_customer_form"):

            customer_id = st.number_input(
                "Customer ID",
                min_value=1,
                step=1
            )

            customer_name = st.text_input(
                "Customer Name"
            )

            phone = st.text_input(
                "Phone"
            )

            city = st.text_input(
                "City"
            )

            submitted = st.form_submit_button(
                "Add Customer"
            )


        if submitted:

            execute_query(
                """
                INSERT INTO customers
                (
                    customer_id,
                    customer_name,
                    phone,
                    city
                )
                VALUES
                (%s, %s, %s, %s)
                """,
                (
                    customer_id,
                    customer_name,
                    phone,
                    city
                ),
                "Customer added successfully! ✅"
            )


    # -----------------------------------------------------
    # CUSTOMER PURCHASE HISTORY
    # -----------------------------------------------------

    elif option == "Customer Purchase History":

        st.subheader(
            "🧾 Customer Purchase History"
        )


        df = fetch_dataframe(
            """
            SELECT DISTINCT customer_name
            FROM sales
            ORDER BY customer_name
            """
        )


        if df.empty:

            st.info(
                "No sales found."
            )

            return


        customer_name = st.selectbox(
            "Select Customer",
            df["customer_name"].tolist()
        )


        history = fetch_dataframe(
            """
            SELECT
                sale_id,
                customer_name,
                plant_name,
                quantity,
                total_amount,
                sale_date
            FROM sales
            WHERE customer_name=%s
            ORDER BY sale_date DESC
            """,
            (customer_name,)
        )


        st.dataframe(
            history,
            use_container_width=True
        )


        if not history.empty:

            total = history[
                "total_amount"
            ].sum()

            st.write(
                f"**Total Purchased Amount: ₹{total:.2f}**"
            )


    # -----------------------------------------------------
    # TRACK CUSTOMER PURCHASES
    # -----------------------------------------------------

    else:

        st.subheader(
            "📊 Track Customer Purchases"
        )


        df = fetch_dataframe(
            """
            SELECT
                customer_name,
                SUM(total_amount)
                AS total_spending
            FROM sales
            GROUP BY customer_name
            ORDER BY total_spending DESC
            """
        )


        if df.empty:

            st.info(
                "No purchase data found."
            )

        else:

            st.dataframe(
                df,
                use_container_width=True
            )


# =========================================================
# BILLING
# =========================================================

def billing_management():

    st.header("💰 Billing")


    customers = fetch_dataframe(
        """
        SELECT customer_name
        FROM customers
        ORDER BY customer_name
        """
    )


    plants = fetch_dataframe(
        """
        SELECT
            plant_id,
            plant_name,
            price,
            quantity
        FROM plants
        ORDER BY plant_name
        """
    )


    if customers.empty:

        st.warning(
            "Please add a customer first."
        )

        return


    if plants.empty:

        st.warning(
            "Please add a plant first."
        )

        return


    # Customer

    customer_name = st.selectbox(
        "Select Customer",
        customers["customer_name"].tolist()
    )


    # Plant

    plant_id = st.selectbox(
        "Select Plant",
        plants["plant_id"].tolist(),

        format_func=lambda x:
        plants[
            plants["plant_id"] == x
        ]["plant_name"].iloc[0]
    )


    selected = plants[
        plants["plant_id"] == plant_id
    ].iloc[0]


    plant_name = selected[
        "plant_name"
    ]


    price = float(
        selected["price"]
    )


    stock = int(
        selected["quantity"]
    )


    st.write(
        f"**Plant:** {plant_name}"
    )


    st.write(
        f"**Price:** ₹{price:.2f}"
    )


    st.write(
        f"**Available Stock:** {stock}"
    )


    # Quantity

    if stock > 0:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=stock,
            value=1,
            step=1
        )

    else:

        st.error(
            "This plant is out of stock."
        )

        return


    total = price * quantity


    st.info(
        f"Total Amount: ₹{total:.2f}"
    )


    # Create bill

    if st.button("Create Bill"):


        if quantity > stock:

            st.error(
                "Not enough stock available."
            )

            return


        connection = None
        cursor = None


        try:

            connection = get_connection()

            cursor = connection.cursor()


            # Insert sale

            cursor.execute(
                """
                INSERT INTO sales
                (
                    customer_name,
                    plant_name,
                    quantity,
                    total_amount,
                    sale_date
                )
                VALUES
                (%s, %s, %s, %s, %s)
                """,
                (
                    customer_name,
                    plant_name,
                    quantity,
                    total,
                    date.today()
                )
            )


            # Reduce stock

            cursor.execute(
                """
                UPDATE plants
                SET quantity = quantity - %s
                WHERE plant_id = %s
                """,
                (
                    quantity,
                    plant_id
                )
            )


            connection.commit()


            st.success(
                "Bill created successfully! 🎉"
            )


            # Bill details

            st.subheader(
                "🧾 Bill Details"
            )


            st.write(
                f"**Customer:** {customer_name}"
            )


            st.write(
                f"**Plant:** {plant_name}"
            )


            st.write(
                f"**Quantity:** {quantity}"
            )


            st.write(
                f"**Price per Plant:** ₹{price:.2f}"
            )


            st.write(
                f"**Total Amount:** ₹{total:.2f}"
            )


            st.write(
                f"**Date:** {date.today()}"
            )


        except Exception as e:

            if connection:
                connection.rollback()

            st.error(
                f"Billing error: {e}"
            )


        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


# =========================================================
# REPORTS
# =========================================================

def reports_management():

    st.header("📊 Reports")


    option = st.selectbox(
        "Choose a report",
        [
            "Total Sales",
            "Available Stock",
            "Low Stock",
            "Customer History"
        ]
    )


    # -----------------------------------------------------
    # TOTAL SALES
    # -----------------------------------------------------

    if option == "Total Sales":

        df = fetch_dataframe(
            """
            SELECT
                COUNT(*) AS total_bills,
                COALESCE(
                    SUM(total_amount), 0
                ) AS total_sales
            FROM sales
            """
        )


        if not df.empty:

            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Total Sales",
                    f"₹{float(df.iloc[0]['total_sales']):.2f}"
                )


            with col2:

                st.metric(
                    "Total Bills",
                    int(df.iloc[0]["total_bills"])
                )


        sales = fetch_dataframe(
            """
            SELECT
                sale_id,
                customer_name,
                plant_name,
                quantity,
                total_amount,
                sale_date
            FROM sales
            ORDER BY sale_date DESC,
                     sale_id DESC
            """
        )


        if not sales.empty:

            st.subheader(
                "Sales Details"
            )

            st.dataframe(
                sales,
                use_container_width=True
            )


    # -----------------------------------------------------
    # AVAILABLE STOCK
    # -----------------------------------------------------

    elif option == "Available Stock":

        df = fetch_dataframe(
            """
            SELECT
                plant_id,
                plant_name,
                category,
                price,
                quantity,
                supplier_name
            FROM plants
            ORDER BY plant_name
            """
        )


        if df.empty:

            st.info(
                "No stock available."
            )

        else:

            st.dataframe(
                df,
                use_container_width=True
            )


    # -----------------------------------------------------
    # LOW STOCK
    # -----------------------------------------------------

    elif option == "Low Stock":

        threshold = st.number_input(
            "Low stock threshold",
            min_value=0,
            value=5,
            step=1
        )


        df = fetch_dataframe(
            """
            SELECT
                plant_id,
                plant_name,
                category,
                quantity,
                supplier_name
            FROM plants
            WHERE quantity <= %s
            ORDER BY quantity
            """,
            (threshold,)
        )


        if df.empty:

            st.success(
                "No low-stock plants."
            )

        else:

            st.warning(
                "Low-stock plants:"
            )

            st.dataframe(
                df,
                use_container_width=True
            )


    # -----------------------------------------------------
    # CUSTOMER HISTORY
    # -----------------------------------------------------

    else:

        df = fetch_dataframe(
            """
            SELECT
                customer_name,
                COUNT(*) AS number_of_purchases,
                SUM(total_amount)
                AS total_spending
            FROM sales
            GROUP BY customer_name
            ORDER BY total_spending DESC
            """
        )


        if df.empty:

            st.info(
                "No customer sales history found."
            )

        else:

            st.dataframe(
                df,
                use_container_width=True
            )


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    st.header(
        "🏠 Welcome to Green Bloom"
    )


    st.write(
        "Manage plants, suppliers, customers, "
        "billing, stock and sales reports."
    )


    # Get plants

    df = fetch_dataframe(
        """
        SELECT
            plant_name,
            price,
            quantity
        FROM plants
        ORDER BY plant_id
        """
    )


    if df.empty:

        st.info(
            "No plants available."
        )

        return


    st.subheader(
        "🌱 Available Plants"
    )


    # Display plants with images

    for start in range(0, len(df), 3):

        cols = st.columns(3)


        for i, col in enumerate(cols):

            index = start + i


            if index >= len(df):

                break


            row = df.iloc[index]


            with col:

                plant_name = str(
                    row["plant_name"]
                )


                image_path = plant_images.get(
                    plant_name
                )


                if image_path:

                    try:

                        st.image(
                            image_path,
                            caption=plant_name,
                            width=200
                        )

                    except Exception:

                        st.write("🌱")

                else:

                    st.write("🌱")


                st.write(
                    f"**{plant_name}**"
                )


                st.write(
                    f"Price: ₹{row['price']}"
                )


                st.write(
                    f"Stock: {row['quantity']}"
                )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title(
    "🌱 Green Bloom"
)


page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🌿 Plant Management",
        "🚚 Supplier Management",
        "👤 Customer Management",
        "💰 Billing",
        "📊 Reports"
    ]
)


# =========================================================
# PAGE SELECTION
# =========================================================

if page == "🏠 Home":

    home_page()


elif page == "🌿 Plant Management":

    plant_management()


elif page == "🚚 Supplier Management":

    supplier_management()


elif page == "👤 Customer Management":

    customer_management()


elif page == "💰 Billing":

    billing_management()


elif page == "📊 Reports":

    reports_management()