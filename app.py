import streamlit as st
import pandas as pd
import joblib
import os
import altair as alt
import calendar
from datetime import datetime # Added for smart defaults

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="Clothing Production AI",
    page_icon="👕",
    layout="centered"
)

MODEL_FILE = 'production_ai_brain.pkl'

# ==========================================
# 2. MODEL LOADING LOGIC
# ==========================================
@st.cache_resource
def load_ai_brain():
    if not os.path.exists(MODEL_FILE):
        st.error(f"🚨 Critical Error: '{MODEL_FILE}' not found.")
        st.warning("Please run 'train_model.py' first to generate the AI brain.")
        st.stop()
    return joblib.load(MODEL_FILE)

# ==========================================
# 3. UI & PREDICTION LOGIC
# ==========================================
def main():
    # --- Header ---
    st.title("👕 Clothing Production Forecaster")
    st.markdown("""
    This AI predicts the **Optimal Production Quantity** for the upcoming season 
    based on historical sales trends.
    """)
    st.divider()

    # --- Load Model ---
    artifacts = load_ai_brain()
    model = artifacts['model']
    le = artifacts['encoder']
    last_training_year = artifacts['last_year']

    # Generate Month Map
    # Result: {'January': 1, 'February': 2, ...}
    month_map = {month: index for index, month in enumerate(calendar.month_name) if month}
    month_list = list(month_map.keys())

    # --- SMART DEFAULT LOGIC ---
    # Get current date to auto-suggest the NEXT month
    today = datetime.now()
    current_month_index = today.month  # 1-12
    
    # Calculate next month (wrap around: if Dec (12), next is Jan (1))
    next_month_index = (current_month_index % 12) + 1
    
    # Get the list index (0-11) for the selectbox
    # next_month_index is 1-12, so we subtract 1 to get list index
    default_list_index = next_month_index - 1

    # Smart Year Logic: If forecasting for next year, adjust year logic if needed
    # (Simple version: use the logic from your artifacts or current date)
    forecast_year = last_training_year + 1

    # --- Sidebar ---
    st.sidebar.header("⚙️ Configuration")
    st.sidebar.info(f"📅 Model Trained Until: **{last_training_year}**")
    
    selected_month = st.sidebar.selectbox(
        "Select Month for Production",
        options=month_list,
        index=default_list_index  # <--- UPDATED: Now defaults to next month
    )
    
    # If user selects a month earlier than current month, they probably mean NEXT year 
    # (e.g. It's Nov 2025, they select Jan. They likely mean Jan 2026, not Jan 2025)
    # You can add logic here if your model supports dynamic years, 
    # but for now we stick to your `future_year` logic.
    
    st.sidebar.write(f"Target: **{selected_month} {forecast_year}**")

    run_forecast = st.button(f"Generate Forecast", type="primary", use_container_width=True)

    # --- Main Logic ---
    if run_forecast:
        with st.spinner("Running AI Prediction..."):
            # 1. Prepare Input Data
            month_num = month_map[selected_month]
            all_products = le.classes_
            
            input_data = pd.DataFrame({
                'Year': [forecast_year] * len(all_products),
                'Month_Num': [month_num] * len(all_products),
                'Product_ID': le.transform(all_products)
            })

            # 2. Predict
            predictions = model.predict(input_data)

            # 3. Format Results
            results = pd.DataFrame({
                'Product Name': all_products,
                'Suggested Quantity': predictions.astype(int)
            })
            
            results = results.sort_values(by='Suggested Quantity', ascending=False).reset_index(drop=True)

            # --- SECTION 1: METRICS ---
            st.subheader(f"🏆 Production Targets: {selected_month} {forecast_year}")
            
            # Dynamic Column Layout
            # If you have many products, 3 columns might get crowded. 
            # This is safe, but consider 'st.columns(4)' if you have >12 products.
            cols = st.columns(3)
            for index, row in results.iterrows():
                col = cols[index % 3]
                col.metric(
                    label=row['Product Name'], 
                    value=f"{row['Suggested Quantity']:,}"
                )

            st.divider()

            # --- SECTION 2: VISUALIZATION ---
            st.subheader("📊 Production Distribution")
            
            chart = alt.Chart(results).mark_bar(cornerRadius=5).encode(
                x=alt.X('Suggested Quantity', title='Quantity'),
                y=alt.Y('Product Name', sort='-x', title='Product'),
                color=alt.Color('Suggested Quantity', scale=alt.Scale(scheme='greens'), legend=None),
                tooltip=['Product Name', 'Suggested Quantity']
            ).properties(height=350)
            
            st.altair_chart(chart, use_container_width=True)

            st.divider()

            # --- SECTION 3: DATA EXPORT ---
            st.subheader("📋 Detailed Data")
            st.dataframe(results, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()