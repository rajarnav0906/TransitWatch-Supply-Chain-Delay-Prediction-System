from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path("delay_predictor_model.pkl")
DEFAULT_SAMPLE = {
    "distance_km": 450,
    "weather": "Rain",
    "vehicle_type": "Truck",
    "vendor_rating": 3,
    "carrier": "Delhivery",
}


def _load_model():
    """Load and cache the regression pipeline."""
    if not hasattr(_load_model, "_cached_model"):
        _load_model._cached_model = joblib.load(MODEL_PATH)
    return _load_model._cached_model


def _prepare_dataframe(payload):
    """Convert the incoming dictionary to a single-row DataFrame."""
    return pd.DataFrame([payload])


def estimate_delay(shipment_params=None):
    """
    Run the trained model for the given shipment description.

    Args:
        shipment_params (dict | None): Optional override for the default sample.
    """
    shipment_payload = shipment_params or dict(DEFAULT_SAMPLE)
    model = _load_model()
    prediction_frame = _prepare_dataframe(shipment_payload)
    estimated_delay = model.predict(prediction_frame)[0]

    explanation = (
        "Based on past patterns, weather and vendor rating may have caused this delay."
    )

    return {
        "input": shipment_payload,
        "predicted_delay_days": round(estimated_delay, 2),
        "reason": explanation,
    }
