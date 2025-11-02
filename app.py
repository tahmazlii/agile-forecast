import streamlit as st
import pandas as pd
import simulator  
import numpy as np 


def load_data_from_upload(uploaded_file):
    """Loads throughput data from an uploaded file."""
    df = pd.read_csv(uploaded_file)
    return df['throughput'].tolist()


st.title('Agile Project Forecaster')
st.markdown("Use Monte Carlo simulation to forecast your project's completion date.")

# sidebar configuration
st.sidebar.header('Simulation Inputs')

uploaded_file = st.sidebar.file_uploader("Upload Throughput CSV", type=["csv"])

remaining_work = st.sidebar.number_input("Tasks/Points Remaining", min_value=1, value=50, step=5)

num_sims = st.sidebar.slider("Number of Simulations", min_value=1000, max_value=50000, value=10000, step=1000)

max_weeks = st.sidebar.number_input("Forecast Horizon (Weeks)", min_value=5, max_value=100, value=20, step=1,
                                    help="How many weeks into the future to simulate.")

run_button = st.sidebar.button("Run Forecast", type="primary")

# app behavior
if run_button and uploaded_file is not None:
    try:

        history = load_data_from_upload(uploaded_file)
        st.write(f"Running {num_sims:,} simulations for {max_weeks} weeks...")
        metrics, chart_fig = simulator.generate_forecast(
            history, remaining_work, num_sims, max_weeks
        )
        st.success("Simulation Complete!")

        # display metrics
        st.subheader(" Probabilistic Forecast")
        col1, col2, col3 = st.columns(3)
        col1.metric("50% Likelihood", metrics["50%"])
        col2.metric("85% Likelihood", metrics["85%"])
        col3.metric("95% Likelihood", metrics["95%"])
        
        # display plot
        st.subheader(" Burn-Up Chart")
        st.pyplot(chart_fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error("Please make sure your CSV is formatted correctly with a 'throughput' column.")
        
elif not run_button:
    st.info("Upload your CSV file and click 'Run Forecast' in the sidebar to start.")