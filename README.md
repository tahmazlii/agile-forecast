## ☁️ Live Demo

**You can try the app live here:** (https://agileforecast.streamlit.app)



# 🚀 Agile Project Forecaster

A web app that uses Monte Carlo simulation to create probabilistic "burn-up" charts and forecast project completion dates.

This tool moves beyond simple "best-case/worst-case" estimates by running thousands of simulations based on your team's actual historical data.

## 🛠️ How to Run Locally

1.  Clone this repository.
2.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## 🏛️ Project Structure
* **`app.py`**: The Streamlit web interface (the "front-end").
* **`simulator.py`**: The back-end simulation "engine".
* **`requirements.txt`**: The list of Python dependencies.
* **`history.csv`**: Sample data to test the app.
