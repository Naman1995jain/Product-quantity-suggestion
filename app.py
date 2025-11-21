import streamlit as st
import pandas as pd
import joblib
import os
import altair as alt  # Added for better charts

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="Clothing Production AI",
    page_icon="👕",
    layout="centered"
)

MODEL_FILE = 'clothing_production_model.joblib'

# ==========================================
# 2. MODEL LOADING LOGIC
# ==========================================
@st.cache_resource
def load_model():
    """
    Loads the pre-trained model artifacts.
    Strictly requires 'clothing_production_model.joblib' to exist.
    """
    if not os.path.exists(MODEL_FILE):
        st.error(f"🚨 Critical Error: Model file '{MODEL_FILE}' not found.")
        st.warning("Please ensure the .joblib file is in the same directory as this app.")
        st.stop()

    return joblib.load(MODEL_FILE)

# ==========================================
# 3. UI & PREDICTION LOGIC
# ==========================================
def main():
    # --- Header ---
    st.title("👕 Clothing Production Forecaster")
    st.markdown("""
    Predicts **Suggested Production Quantity** for the upcoming month.
    """)
    st.divider()

    # --- Load Model ---
    artifacts = load_model()
    model = artifacts['model']
    product_encoder = artifacts['product_encoder']
    month_map = artifacts['month_map']

    # --- Sidebar ---
    st.sidebar.header("⚙️ Configuration")
    selected_month = st.sidebar.selectbox(
        "Select Month for Production",
        options=list(month_map.keys()),
        index=10 # Default to November
    )
    
    run_forecast = st.button(f"Generate Forecast for {selected_month}", type="primary", use_container_width=True)

    # --- Main Logic ---
    if run_forecast:
        
        # 1. Prepare Input
        month_num = month_map[selected_month]
        all_products = product_encoder.classes_
        
        input_data = pd.DataFrame({
            'Month_Num': [month_num] * len(all_products),
            'Product_Encoded': product_encoder.transform(all_products)
        })

        # 2. Predict
        predictions = model.predict(input_data)

        # 3. Format
        results = pd.DataFrame({
            'Product Name': all_products,
            'Suggested Quantity': predictions.astype(int)
        })
        
        # Sort: Highest quantity first
        results = results.sort_values(by='Suggested Quantity', ascending=False).reset_index(drop=True)

        # --- SECTION 1: SUGGESTIONS (Metrics) ---
        st.subheader(f"🏆 Suggestions for {selected_month}")
        
        # Display metrics in a grid of 3 columns
        cols = st.columns(3)
        for index, row in results.iterrows():
            col = cols[index % 3]
            col.metric(
                label=row['Product Name'], 
                value=f"{row['Suggested Quantity']:,}"
            )

        st.divider()

        # --- SECTION 2: VISUALIZATION (Full Width) ---
        st.subheader("📊 Production Trends")
        
        # Create a clean horizontal bar chart using Altair
        chart = alt.Chart(results).mark_bar(cornerRadius=5).encode(
            x=alt.X('Suggested Quantity', title='Quantity'),
            y=alt.Y('Product Name', sort='-x', title='Product'), # Sorts by quantity
            color=alt.Color('Suggested Quantity', scale=alt.Scale(scheme='greens'), legend=None),
            tooltip=['Product Name', 'Suggested Quantity']
        ).properties(
            height=350 # Fixed height for better visibility
        )
        
        st.altair_chart(chart, use_container_width=True)

        st.divider()

        # --- SECTION 3: DETAILED LIST (Full Width) ---
        st.subheader("📋 Detailed Production List")
        st.dataframe(
            results, 
            use_container_width=True,
            hide_index=True
            # removed height=None to fix the error
        )

if __name__ == "__main__":
    main()