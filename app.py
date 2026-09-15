import pandas as pd
import numpy as np
import streamlit as st

from db_function import (
    connect_to_db,
    get_basic_info,
    get_additonal_tables,
    add_new_manual_id,
    get_categories,
    get_suppliers,
    get_all_products,
    get_product_history,
    Place_reorder,
    get_pending_reorders
)

# sidebar
st.sidebar.title("Inventory Management Dashboard")
option = st.sidebar.radio("Select Option:", ["Basic Information", "Operational Task"])

# main space
st.title("Inventory Management Dashboard")
db = connect_to_db()
cursor = db.cursor(dictionary=True)

# -------------- basic information page -------------
if option == "Basic Information":
    st.header("Basic Metrics")

    # get basic information from db
    basic_info = get_basic_info(cursor)

    cols = st.columns(3)
    keys = list(basic_info.keys())

    for i in range(3):
        cols[i].metric(label=keys[i], value=basic_info[keys[i]])

    cols = st.columns(3)
    for i in range(3, 6):
        cols[i - 3].metric(label=keys[i], value=basic_info[keys[i - 3]])
    st.divider()

    # fetch and display detailed table
    tables = get_additonal_tables(cursor)
    for labels, data in tables.items():
        st.header(labels)
        df = pd.DataFrame(data)
        st.dataframe(df)
        st.divider()

# -------------- operational task page -------------
if option == "Operational Task":
    st.header("Operational Tasks")
    Selected_task = st.selectbox("Choose a Task",
                                 ["Add New Product", "Product History", "Place Reorder", "Receive Reorder"])

    if Selected_task == "Add New Product":
        st.header("Add New Product")
        categories = get_categories(cursor)
        suppliers = get_suppliers(cursor)

        with st.form("Add_Product_Form"):
            product_name = st.text_input("Product_Name")
            product_category = st.selectbox("Category", categories)
            product_price = st.number_input("Price", min_value=0.0)
            product_stock = st.number_input("Stock", min_value=0.0, step=1.0)
            product_level = st.number_input("Level", min_value=0.0, step=1.0)

            supplier_ids = [s["supplier_id"] for s in suppliers]
            supplier_names = [s["supplier_name"] for s in suppliers]

            selected_supplier_id = st.selectbox(
                "Suppliers",
                options=supplier_ids,
                format_func=lambda x: supplier_names[supplier_ids.index(x)]
            )
            submitted = st.form_submit_button("Submit")

            if submitted:
                if not product_name.strip():
                    st.error("Product Name cannot be empty")
                else:
                    try:
                        add_new_manual_id(
                            cursor,
                            db,
                            product_name,
                            product_category,
                            product_price,
                            int(product_stock),
                            int(product_level),
                            selected_supplier_id
                        )
                        st.success(f"Product '{product_name}' Added Successfully")
                    except Exception as e:
                        st.error(f"Error adding the product: {e}")

    # ------------------------- product History ------------------------
    elif Selected_task == "Product History":
        st.header("Product History")

        # get product list
        products = get_all_products(cursor)
        product_names = [p['product_name'] for p in products]
        product_ids = [p['product_id'] for p in products]

        # Added selectbox so user can pick which product history to see
        selected_product_name = st.selectbox("Select Product", product_names)

        if selected_product_name:
            # Fixed typos: mapping the correct selected name to its ID
            selected_product_id = product_ids[product_names.index(selected_product_name)]
            history_data = get_product_history(cursor, selected_product_id)

            if history_data:
                df = pd.DataFrame(history_data)
                st.dataframe(df)
            else:
                st.info("Product History Not Found")

#------------------Place Reorder -------------------
    if Selected_task == "Place Reorder":
        st.header("Place Reorder")

        products = get_all_products(cursor)
        product_names = [p['product_name'] for p in products]
        product_ids = [p['product_id'] for p in products]

        selected_product_name = st.selectbox("Select Product", product_names)
        reorder_quantity = st.number_input("Reorder Quantity", min_value=1, step=1)

        if st.button("Reorder"):
            if not selected_product_name:
                st.error("Product Name cannot be empty")
            elif reorder_quantity <= 0:
                st.error("Reorder Quantity must be greater than 0")
            else:
                selected_product_id = product_ids[product_names.index(selected_product_name)]
                try:
                    Place_reorder(
                        cursor,
                        db,
                        selected_product_id,
                        reorder_quantity
                    )
                    st.success(f"Product '{selected_product_name}' Reordered Successfully")

                except Exception as e:
                    st.error(f"Error reordering the product: {e}")

#----------------RECEIVING AN ORDER ------------------
    elif Selected_task == "Receive Reorder":
        st.header("Mark Reorder as Received")

        pending_reorders = get_pending_reorders(cursor)

        if not pending_reorders:
            st.info("No Pending Orders to Receive.")
        else:
            reorder_options = {
                f"ID {r['reorder_id']} - {r['product_name']}": r['reorder_id']
                for r in pending_reorders
            }

            selected_label = st.selectbox(
                "Select Reorder to mark as Received",
                options=list(reorder_options.keys())
            )

            selected_reorder_id = reorder_options[selected_label]

            if st.button("Mark as Received"):
                try:
                    mark_reorder_as_received(
                        cursor,
                        db,
                        selected_reorder_id
                    )

                    st.success(
                        f"Reorder ID {selected_reorder_id} marked as received"
                    )

                except Exception as e:
                    st.error(f"Error: {e}")













