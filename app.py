import streamlit as st
import pandas as pd
import os

# File to store results
RESULTS_FILE = "calculator_results.csv"

# Function to save results
def save_result(operation, result):
    if not os.path.exists(RESULTS_FILE):
        df = pd.DataFrame(columns=["Operation", "Result"])
    else:
        df = pd.read_csv(RESULTS_FILE)

    new_entry = {"Operation": operation, "Result": result}
    df = df.append(new_entry, ignore_index=True)
    df.to_csv(RESULTS_FILE, index=False)

# Main app
st.title("Simple Calculator")

# User inputs
num1 = st.number_input("Enter the first number:", value=0.0)
num2 = st.number_input("Enter the second number:", value=0.0)
operation = st.selectbox("Select an operation:", ["Addition", "Subtraction", "Multiplication", "Division"])

# Perform calculation
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

# Display and save result
if st.button("Calculate"):
    if result is not None:
        st.success(f"The result of {operation} is: {result}")
        save_result(f"{num1} {operation} {num2}", result)

# Function to save results
def save_result(operation, result):
    if not os.path.exists(RESULTS_FILE):
        df = pd.DataFrame(columns=["Operation", "Result"])
    else:
        df = pd.read_csv(RESULTS_FILE)

    new_entry = pd.DataFrame({"Operation": [operation], "Result": [result]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(RESULTS_FILE, index=False)

