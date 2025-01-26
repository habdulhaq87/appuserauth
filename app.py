import streamlit as st
import pandas as pd
import sqlite3
import hashlib

# Database setup
DB_FILE = "user_data.db"

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create users table
def create_users_table():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                username TEXT,
                operation TEXT,
                result REAL,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        """)

# Function to register a new user
def register_user(username, password):
    with sqlite3.connect(DB_FILE) as conn:
        hashed_password = hash_password(password)
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))

# Function to verify user credentials
def verify_user(username, password):
    with sqlite3.connect(DB_FILE) as conn:
        hashed_password = hash_password(password)
        result = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password)).fetchone()
        return result is not None

# Function to save calculation results
def save_result(username, operation, result):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO results (username, operation, result) VALUES (?, ?, ?)", (username, operation, result))

# Function to retrieve user results
def get_user_results(username):
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT operation, result FROM results WHERE username = ?", conn, params=(username,))
    return df

# Main app
def main():
    st.title("Calculator with User Authentication")

    # Tabs for Login, Signup, and Calculator
    menu = ["Login", "Signup", "Calculator"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Signup":
        st.subheader("Create a New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            create_users_table()
            try:
                register_user(new_user, new_password)
                st.success("Account created successfully!")
                st.info("You can now login.")
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose a different username.")

    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            create_users_table()
            if verify_user(username, password):
                st.success(f"Welcome, {username}!")
                # Save the username in session state
                st.session_state["username"] = username
            else:
                st.error("Invalid username or password.")

    elif choice == "Calculator":
        if "username" in st.session_state:
            username = st.session_state["username"]
            st.subheader(f"Hello, {username}! Use the Calculator Below:")

            # Calculator interface
            num1 = st.number_input("Enter the first number:", value=0.0)
            num2 = st.number_input("Enter the second number:", value=0.0)
            operation = st.selectbox("Select an operation:", ["Addition", "Subtraction", "Multiplication", "Division"])
            result = None

            if operation == "Addition":
                result = num1 + num2
            elif operation == "Subtraction":
                result = num1 - num2
            elif operation == "Multiplication":
                result = num1 * num2
            elif operation == "Division":
                if num2 != 0:
                    result = num1 / num2
                else:
                    st.error("Division by zero is not allowed.")

            # Perform calculation and save result
            if st.button("Calculate"):
                if result is not None:
                    st.success(f"The result of {operation} is: {result}")
                    save_result(username, f"{num1} {operation} {num2}", result)

            # Show user's saved results
            if st.checkbox("Show My Results"):
                user_results = get_user_results(username)
                if not user_results.empty:
                    st.dataframe(user_results)
                else:
                    st.info("No results found.")
        else:
            st.warning("You must log in to access the Calculator.")

# Run the app
if __name__ == "__main__":
    main()
