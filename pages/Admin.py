"""Password-protected order management view.

Accessible at the /Admin URL of the running app. Requires the
ADMIN_PASSWORD environment variable to be set; without it, the page
refuses to show any order data.
"""
import os

import streamlit as st

import backend

st.set_page_config(page_title="Order Admin", page_icon=":material/lock:", layout="wide")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

st.title("Order Management")

if not ADMIN_PASSWORD:
    st.error(
        "ADMIN_PASSWORD is not set on the server. Set this environment variable "
        "before this page can be used, so order data stays protected."
    )
    st.stop()

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    entered_password = st.text_input("Admin password", type="password")
    if st.button("Log in"):
        if entered_password == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

if st.button("Log out"):
    st.session_state.admin_authenticated = False
    st.rerun()

orders = backend.get_all_orders()
st.caption(f"{len(orders)} order(s) total.")

status_options = ["new", "confirmed", "fulfilled", "cancelled"]

for order in orders:
    with st.expander(
        f"Order #{order['id']} - {order['customer_name']} - "
        f"₹{order['total_amount']:,.0f} - {order['order_status']}"
    ):
        st.write(f"**Placed:** {order['created_at']}")
        st.write(f"**Phone:** {order['customer_phone']}")
        if order["notes"]:
            st.write(f"**Notes:** {order['notes']}")
        st.write("**Items:**")
        for item in order["items"]:
            st.write(
                f"- {item['product']} ({item['size']}) x{item['quantity']} "
                f"@ {item['price']}"
            )
        st.write(f"**Payment status:** {order['payment_status']}")
        new_status = st.selectbox(
            "Order status",
            status_options,
            index=status_options.index(order["order_status"])
            if order["order_status"] in status_options
            else 0,
            key=f"status_{order['id']}",
        )
        if st.button("Update status", key=f"update_{order['id']}"):
            backend.update_order_status(order["id"], new_status)
            st.rerun()

if not orders:
    st.info("No orders yet.")
