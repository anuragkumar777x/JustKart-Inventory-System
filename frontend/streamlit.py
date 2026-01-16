import streamlit as st
import requests
import pandas as pd

# ================= CONFIG =================
st.set_page_config(
    page_title="Inventory Cart System",
    page_icon="🛒",
    layout="wide"
)

API_URL = "https://justkart-inventory-system.onrender.com" # FastAPI base URL

def login_user(username, password):
    return requests.post(
        f"{API_URL}/login",
        json={"username": username, "password": password}
    )

def register_user(username, password):
    return requests.post(
        f"{API_URL}/register",
        json={"username": username, "password": password}
    )

def get_error_message(res):
    try:
        data = res.json()
        return data.get("detail") or data.get("error")
    except Exception:
        return None

# ================= HELPERS =================
def get_products():
    try:
        res = requests.get(
            f"{API_URL}/products/{st.session_state.user_id}"
)
        return res.json()
    except:
        return []

def add_product(data):
    return requests.post(f"{API_URL}/add_product", json=data)

def delete_product(pid):
    return requests.delete(f"{API_URL}/delete/{pid}")

def update_product(pid, data):
    return requests.put(f"{API_URL}/edit_product/{pid}", json=data)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

st.title("🛒 JustKart Inventory System")
if not st.session_state.logged_in:
    st.title("🔐 JustKart Login")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = login_user(username, password)

            if res.status_code == 200:
              data = res.json()
              st.session_state.logged_in = True
              st.session_state.user_id = data["user_id"]
              st.session_state.username = data["username"]
              st.success("Login successful")
              st.rerun()
            else:
              st.error(get_error_message(res) or "Invalid username or password")


    
    with tab_register:
        if "new_username" not in st.session_state:
            st.session_state["new_username"] = ""
        if "new_password" not in st.session_state:
            st.session_state["new_password"] = ""

        new_username = st.text_input("New Username", value=st.session_state["new_username"])
        new_password = st.text_input("New Password", type="password", value=st.session_state["new_password"])

        if st.button("Register"):
            if not new_username.strip() or not new_password.strip():
                st.error("Username and password are required")
            else:
                res = register_user(new_username, new_password)

                if res.status_code == 200:
                 st.success("Registered successfully. Please login.")
                else:
                 st.error(get_error_message(res) or "Registration failed")

    st.stop()  # ⛔ VERY IMPORTANT

st.sidebar.write(f"👤 Hello, {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.rerun()

st.caption("Track • Manage • Grow your inventory in real time")
st.divider()

tab1, tab2 = st.tabs(["➕ Add Product", "🛍️ Your Cart"])

# ================= ADD PRODUCT =================
with tab1:
    if "product_added" not in st.session_state:
        st.session_state.product_added = False

    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Product Name", placeholder="")
        description = st.text_area("Description", placeholder="Short product description")
        price = st.number_input("Price", min_value=0.0, value=None, placeholder="Enter price")
        quantity = st.number_input("Quantity", min_value=1, help="Minimum quantity is 1")

        submitted = st.form_submit_button("Add Product")

        if submitted:
            if not name.strip():
                st.error("Product name is required")
            elif price is None:
                st.error("Price is required")
            elif quantity <= 0:
                st.error("Quantity must be greater than 0")
            else:
                payload = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "quantity": quantity
                }
                res = requests.post(
                    f"{API_URL}/add_product",
                    json=payload,
                    params={"user_id": st.session_state.user_id}
                )
                if res.status_code == 200:
                    st.session_state.product_added = True
                else:
                    st.error("❌ Failed to add product")

    if st.session_state.product_added:
        st.success("✅ Product added successfully")
        st.session_state.product_added = False

# ================= YOUR CART =================
with tab2:
    st.subheader("Your Cart")

    products = get_products()

    if not products:
        st.info("🛒 Cart is empty")
    else:
        df = pd.DataFrame(products)

        # 🔍 Search
        search = st.text_input(
            "🔍 Search products",
            placeholder="Type product name..."
        )
        if search:
            df = df[df["name"].str.contains(search, case=False)]

        # 📊 Cart Summary
        st.markdown("### 📊 Cart Summary")

        colA, colB, colC = st.columns(3)
        colA.metric("🧾 Total Products", len(df))
        colB.metric("📦 Total Quantity", int(df["quantity"].sum()))
        colC.metric(
            "💰 Total Value",
            f"₹ {(df['price'] * df['quantity']).sum():.2f}"
        )

        st.divider()

        # 📋 Product Table
        st.dataframe(df, width="stretch")

    st.markdown("---")
    st.subheader("🛠️ Manage Products")
    st.caption("Use Product ID from the table above")

    col1, col2 = st.columns(2)

    with col1:
        pid = st.number_input(
            "Product ID",
            min_value=1,
            step=1,
            value=None,
            placeholder="Enter product ID"
        )
        if st.button("🗑️ Delete Product", disabled=pid is None):
            r = delete_product(pid)
            if r.status_code == 200:
                st.toast("🗑️ Product deleted successfully")
                st.rerun()
            else:
                st.error("Delete failed")

    with col2:
        st.markdown("### ✏️ Edit Product")
        new_name = st.text_input("New Name")
        new_desc = st.text_input("New Description")
        new_price = st.number_input("New Price", min_value=0.0, value=None, placeholder="Enter new price")
        new_qty = st.number_input("New Quantity", min_value=1)

        if st.button("Update Product", disabled=pid is None):
            payload = {
                "name": new_name or None,
                "description": new_desc or None,
                "price": new_price,
                "quantity": new_qty
            }
            r = update_product(pid, payload)
            if r.status_code == 200:
                st.toast("✏️ Product updated successfully")
                st.rerun()
            else:
                st.error("Update failed")
