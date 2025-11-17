# TransitWatch: Supply Chain Delay Prediction System

A web application that helps logistics teams predict shipment delays before they happen. Built with Flask and machine learning, it analyzes factors like distance, weather conditions, vehicle type, and vendor performance to forecast potential delays.

## What It Does

- Predicts how many days a shipment might be delayed
- Considers real-world factors: weather, distance, vehicle type, carrier quality, and vendor ratings
- Suggests alternative routes or transport modes when delays are likely
- Generates downloadable reports in PDF or CSV format

## How It Works

The system uses a Random Forest machine learning model trained on historical shipment data. You input details about your shipment, and it predicts the delay based on patterns it learned from similar past shipments.

**Input factors:**
- Distance (in kilometers)
- Weather conditions (Sunny, Rain, Storm, Fog)
- Vehicle type (Truck, Van, Bike)
- Vendor rating (1-5 scale)
- Carrier name

**Output:**
- Predicted delay in days
- Explanation of likely causes
- Risk assessment and recommendations

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Train the model (if needed):
   ```bash
   python model_workbench.py
   ```

3. Generate sample data (optional):
   ```bash
   python fake_data_factory.py
   ```

4. Run the application:
   ```bash
   python supply_dashboard.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000`

## Project Files

- `supply_dashboard.py` - Main Flask web application
- `delay_engine.py` - Core prediction logic
- `model_workbench.py` - Model training script
- `fake_data_factory.py` - Generates synthetic training data
- `sample_shipments.py` - Sample shipment data
- `delay_predictor_model.pkl` - Trained ML model
- `shipment_data.csv` - Training dataset

## Technology Stack

- **Backend:** Flask (Python)
- **Machine Learning:** Scikit-learn (Random Forest Regressor)
- **Data Processing:** Pandas
- **PDF Generation:** xhtml2pdf

## Notes

The model is trained on synthetic data. For production use, replace it with real historical shipment data to improve accuracy.
