import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sympy import symbols, Eq, solve
from scipy import special
from math import factorial as math_factorial

# Set page configuration
st.set_page_config(page_title="Complex Advanced Calculator", layout="wide")

# Title and description
st.title("Complex Advanced Calculator")
st.markdown("""
This advanced calculator offers a range of functionalities including basic arithmetic, scientific calculations, graphing, unit conversion, equation solving, and history analysis. Use the sidebar to navigate between different functionalities.
""")

# Sidebar for navigation
st.sidebar.header("Options")
function = st.sidebar.selectbox("Select Function", [
    "Basic Arithmetic", "Scientific", "Graphing", "Unit Conversion", "Equation Solver", "History Analysis"
])

# History management
if 'history' not in st.session_state:
    st.session_state.history = []

def add_to_history(entry):
    st.session_state.history.append(entry)

def reset_history():
    st.session_state.history = []

# Function for basic arithmetic
def basic_arithmetic():
    st.subheader("Basic Arithmetic Operations")

    # Input fields
    num1 = st.number_input("Enter first number", format="%.2f")
    num2 = st.number_input("Enter second number", format="%.2f")
    operation = st.radio("Select operation", ["Addition", "Subtraction", "Multiplication", "Division"])

    # Perform calculation
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
            result = "Error: Division by zero"

    st.write(f"Result: {result}")
    add_to_history(f"{num1} {operation} {num2} = {result}")

# Function for scientific calculations
def scientific_calculations():
    st.subheader("Scientific Calculations")

    # Input field
    num = st.number_input("Enter number", format="%.2f")

    # Radio button for operation selection
    operation = st.radio("Select operation", [
        "Square Root", "Exponentiation", "Logarithm", "Sine", "Cosine", "Tangent", 
        "Factorial", "Combinations", "Permutations", "Hyperbolic Sine", "Hyperbolic Cosine"
    ])

    # Perform calculation
    if operation == "Square Root":
        result = np.sqrt(num)
    elif operation == "Exponentiation":
        power = st.number_input("Enter power", format="%.2f")
        result = np.power(num, power)
    elif operation == "Logarithm":
        base = st.number_input("Enter base", format="%.2f")
        result = np.log(num) / np.log(base) if base > 0 and base != 1 else "Error: Invalid base"
    elif operation == "Sine":
        result = np.sin(np.radians(num))
    elif operation == "Cosine":
        result = np.cos(np.radians(num))
    elif operation == "Tangent":
        result = np.tan(np.radians(num))
    elif operation == "Factorial":
        try:
            result = math_factorial(int(num)) if num.is_integer() and num >= 0 else "Error: Factorial is defined for non-negative integers"
        except ValueError:
            result = "Error: Factorial is too large"
    elif operation == "Combinations":
        n = st.number_input("Enter n", format="%.2f")
        k = st.number_input("Enter k", format="%.2f")
        result = special.comb(n, k) if n >= k else "Error: n must be greater than or equal to k"
    elif operation == "Permutations":
        n = st.number_input("Enter n", format="%.2f")
        k = st.number_input("Enter k", format="%.2f")
        result = special.perm(n, k) if n >= k else "Error: n must be greater than or equal to k"
    elif operation == "Hyperbolic Sine":
        result = np.sinh(num)
    elif operation == "Hyperbolic Cosine":
        result = np.cosh(num)

    st.write(f"Result: {result}")
    add_to_history(f"{operation}({num}) = {result}")

# Function for graphing
def graphing():
    st.subheader("Graphing Function")

    # Input field for function
    equation = st.text_input("Enter function (e.g., x**2, np.sin(x))", value="np.sin(x)")

    # Input fields for graph customization
    color = st.color_picker("Select line color", "#0000FF")
    line_style = st.selectbox("Select line style", ["-", "--", "-.", ":"])
    x_min = st.number_input("X Min", -10.0, 0.0)
    x_max = st.number_input("X Max", 0.0, 10.0)
    x = np.linspace(x_min, x_max, 400)

    # Plotting
    try:
        y = eval(equation)
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, color=color, linestyle=line_style)
        plt.title(f"Graph of {equation}")
        plt.xlabel("X")
        plt.ylabel("Y")
        st.pyplot()
    except Exception as e:
        st.error(f"Error: {e}")

# Function for unit conversion
def unit_conversion():
    st.subheader("Unit Conversion")

    # Conversion options
    category = st.selectbox("Select category", ["Length", "Weight", "Temperature"])

    units_dict = {
        "Length": ["meters", "kilometers", "miles", "yards"],
        "Weight": ["grams", "kilograms", "pounds", "ounces"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
    }

    units = units_dict[category]
    
    from_unit = st.selectbox("From unit", units)
    to_unit = st.selectbox("To unit", units)
    value = st.number_input(f"Enter value in {from_unit}", format="%.2f")

    conversion_factors = {
        "Length": {
            ("meters", "kilometers"): 0.001, ("meters", "miles"): 0.000621371, ("meters", "yards"): 1.09361,
            ("kilometers", "meters"): 1000, ("kilometers", "miles"): 0.621371, ("kilometers", "yards"): 1093.61,
            ("miles", "meters"): 1609.34, ("miles", "kilometers"): 1.60934, ("miles", "yards"): 1760,
            ("yards", "meters"): 0.9144, ("yards", "kilometers"): 0.0009144, ("yards", "miles"): 0.000568182
        },
        "Weight": {
            ("grams", "kilograms"): 0.001, ("grams", "pounds"): 0.00220462, ("grams", "ounces"): 0.035274,
            ("kilograms", "grams"): 1000, ("kilograms", "pounds"): 2.20462, ("kilograms", "ounces"): 35.274,
            ("pounds", "grams"): 453.592, ("pounds", "kilograms"): 0.453592, ("pounds", "ounces"): 16,
            ("ounces", "grams"): 28.3495, ("ounces", "kilograms"): 0.0283495, ("ounces", "pounds"): 0.0625
        },
        "Temperature": {
            ("Celsius", "Fahrenheit"): lambda c: c * 9/5 + 32, ("Celsius", "Kelvin"): lambda c: c + 273.15,
            ("Fahrenheit", "Celsius"): lambda f: (f - 32) * 5/9, ("Fahrenheit", "Kelvin"): lambda f: (f - 32) * 5/9 + 273.15,
            ("Kelvin", "Celsius"): lambda k: k - 273.15, ("Kelvin", "Fahrenheit"): lambda k: (k - 273.15) * 9/5 + 32
        }
    }

    if category in ["Length", "Weight"]:
        factor = conversion_factors[category].get((from_unit, to_unit), 1)
        converted_value = value * factor
        st.write(f"{value} {from_unit} = {converted_value:.2f} {to_unit}")
    else:  # Temperature
        convert_func = conversion_factors[category].get((from_unit, to_unit), lambda x: x)
        converted_value = convert_func(value)
        st.write(f"{value} {from_unit} = {converted_value:.2f} {to_unit}")

# Function for equation solving
def equation_solver():
    st.subheader("Equation Solver")

    # Input field for equation
    equation = st.text_input("Enter equation (e.g., x**2 - 4 = 0)")

    # Solve equation
    try:
        x = symbols('x')
        eq = Eq(eval(equation.split('=')[0].strip()), eval(equation.split('=')[1].strip()))
        solutions = solve(eq, x)
        st.write(f"Solutions: {solutions}")
        add_to_history(f"Solved equation {equation} with solutions {solutions}")
    except Exception as e:
        st.error(f"Error: {e}")

# Function for history analysis
def history_analysis():
    st.subheader("History Analysis")

    if len(st.session_state.history) == 0:
        st.write("No history available.")
        return

    # Display history
    for entry in st.session_state.history:
        st.write(entry)

    # Option to clear history
    if st.button("Clear History"):
        reset_history()
        st.write("History cleared!")

# Display selected function
if function == "Basic Arithmetic":
    basic_arithmetic()
elif function == "Scientific":
    scientific_calculations()
elif function == "Graphing":
    graphing()
elif function == "Unit Conversion":
    unit_conversion()
elif function == "Equation Solver":
    equation_solver()
elif function == "History Analysis":
    history_analysis()
