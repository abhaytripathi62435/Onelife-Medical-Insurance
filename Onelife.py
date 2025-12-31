import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Function to categorize income
# -------------------------------
def categorize_income(income):
    """Categorizes income into predefined income groups based on monthly income."""
    if income <= 15000:
        return 'Low Income (15K/month - 3 Lakh/year)'
    elif income <= 25000:
        return 'Middle-Low Income (25K - 5 Lakh/year)'
    elif income <= 30000:
        return 'Middle Income (30K - 7 Lakh/year)'
    elif income <= 40000:
        return 'Upper-Middle Income (40K - 9 Lakh/year)'
    else:
        return 'High Income (50K - 10 Lakh/year)'


# ----------------------------------
# Function to calculate monthly premium
# ----------------------------------
def calculate_monthly_premium(income):
    """Calculate monthly premium as 5% of monthly income."""
    return income * 0.05


# ----------------------------------
# Function to calculate future benefits
# ----------------------------------
def calculate_future_benefits(coverage, years, growth_rate=0.05):
    """Calculate future benefits with compound growth."""
    return coverage * ((1 + growth_rate) ** years)


# ------------------------------------------------
# Function to predict insurance coverage & benefits
# ------------------------------------------------
def predict_insurance_coverage(income, years):
    income_category = categorize_income(income)
    monthly_premium = calculate_monthly_premium(income)

    coverage_dict = {
        'Low Income (15K/month - 3 Lakh/year)': {'accident': 100000, 'health': 50000},
        'Middle-Low Income (25K - 5 Lakh/year)': {'accident': 200000, 'health': 75000},
        'Middle Income (30K - 7 Lakh/year)': {'accident': 300000, 'health': 100000},
        'Upper-Middle Income (40K - 9 Lakh/year)': {'accident': 400000, 'health': 150000},
        'High Income (50K - 10 Lakh/year)': {'accident': 500000, 'health': 200000},
    }

    coverage = coverage_dict.get(income_category, {'accident': 0, 'health': 0})
    accident_coverage = coverage['accident']
    health_coverage = coverage['health']

    future_accident_coverage = calculate_future_benefits(accident_coverage, years)
    future_health_coverage = calculate_future_benefits(health_coverage, years)

    return (
        income_category,
        monthly_premium,
        accident_coverage,
        future_accident_coverage,
        health_coverage,
        future_health_coverage,
    )


# ===============================
# Streamlit UI
# ===============================
st.title("ONELIFE Insurance Package and Coverage Prediction System")

st.write(
    "Enter your details to get a personalized prediction for accident and health insurance coverage."
)

# User Inputs
age = st.number_input("Age", min_value=18, max_value=100, value=30)
sex = st.selectbox("Sex", ["Male", "Female", "Other"])
family_members = st.number_input("Number of Family Members", min_value=1, max_value=10, value=3)
family_details = st.text_area("List of Family Members (optional)")

income = st.number_input(
    "Monthly Income (in INR)", min_value=10000, max_value=5000000, value=50000
)

years = st.number_input(
    "Number of Years for Future Benefits Calculation",
    min_value=1,
    max_value=50,
    value=10,
)

# Prediction Button
if st.button("Predict Insurance Package and Benefits"):
    (
        income_category,
        monthly_premium,
        accident_coverage,
        future_accident_coverage,
        health_coverage,
        future_health_coverage,
    ) = predict_insurance_coverage(income, years)

    # Display Results
    st.subheader("Insurance Prediction Results")
    st.write(f"**Income Category:** {income_category}")
    st.write(f"**Monthly Premium:** ₹{monthly_premium:.2f}")
    st.write(f"**Accident Coverage (Initial):** ₹{accident_coverage:,.2f}")
    st.write(f"**Health Coverage (Initial):** ₹{health_coverage:,.2f}")
    st.write(
        f"**Future Accident Coverage (after {years} years):** ₹{future_accident_coverage:,.2f}"
    )
    st.write(
        f"**Future Health Coverage (after {years} years):** ₹{future_health_coverage:,.2f}"
    )

    # Visualization
    years_range = np.arange(1, years + 1)
    future_accident_benefits = [
        calculate_future_benefits(accident_coverage, year) for year in years_range
    ]
    future_health_benefits = [
        calculate_future_benefits(health_coverage, year) for year in years_range
    ]

    st.subheader("Growth of Accident and Health Benefits Over Time")

    fig, ax = plt.subplots()
    ax.plot(years_range, future_accident_benefits, marker='o', label='Accident Coverage')
    ax.plot(years_range, future_health_benefits, marker='o', label='Health Coverage')
    ax.set_xlabel("Years")
    ax.set_ylabel("Coverage Amount (INR)")
    ax.set_title("Insurance Coverage Growth Over Time")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    st.info(
        "Note: Age, sex, and family details are collected for future enhancements "
        "but are not currently used in coverage calculations."
    )
