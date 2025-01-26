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

    # Create a new entry
    new_entry = pd.DataFrame({"Operation": [operation], "Result": [result]})
    # Concatenate with existing DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)
    # Save back to the CSV file
    df.to_csv(RESULTS_FILE, index=False)

# Main Streamlit app
def main():
    st.title("Simple Calculator")

    # Input fields for numbers
    num1 = st.number_input("Enter the first number:", value=0.0)
    num2 = st.number_input("Enter the second number:", value=0.0)
    # Dropdown for operation selection
    operation = st.selectbox("Select an operation:", ["Addition", "Subtraction", "Multiplication", "Division"])

    # Variable to store the result
    result = None

    # Perform the selected operation
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

    # Display and save the result when Calculate button is clicked
    if st.button("Calculate"):
        if result is not None:
            st.success(f"The result of {operation} is: {result}")
            save_result(f"{num1} {operation} {num2}", result)

    # Option to display saved results
    if st.checkbox("Show saved results"):
        if os.path.exists(RESULTS_FILE):
            df = pd.read_csv(RESULTS_FILE)
            st.dataframe(df)
        else:
            st.info("No results saved yet.")

# Run the app
if __name__ == "__main__":
    main()
