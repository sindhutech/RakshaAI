import streamlit as st
import pandas as pd
import os


def authentication():

    st.sidebar.title("User Authentication")

    menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

    # Create users.csv if it does not exist
    if not os.path.exists("users.csv"):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv("users.csv", index=False)

    users = pd.read_csv("users.csv")

    # Clean username and password columns
    users["username"] = users["username"].astype(str).str.strip()
    users["password"] = users["password"].astype(str).str.strip()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # -----------------------------
    # SIGN UP
    # -----------------------------
    if menu == "Sign Up":

        st.sidebar.subheader("Create Account")

        new_user = st.sidebar.text_input("Username")
        new_pass = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Create Account"):

            new_user = new_user.strip()
            new_pass = new_pass.strip()

            if new_user in users["username"].values:
                st.sidebar.error("User already exists")

            else:

                new_data = pd.DataFrame({
                    "username": [new_user],
                    "password": [new_pass]
                })

                users = pd.concat([users, new_data], ignore_index=True)

                users.to_csv("users.csv", index=False)

                st.sidebar.success("Account created successfully!")

    # -----------------------------
    # LOGIN
    # -----------------------------
    if menu == "Login":

        st.sidebar.subheader("Login")

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):

            username = username.strip()
            password = password.strip()

            user = users[
                (users["username"] == username) &
                (users["password"] == password)
            ]

            if not user.empty:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.sidebar.success("Login successful!")

            else:
                st.sidebar.error("Invalid credentials")

    return st.session_state.logged_in