import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = "shipment_data.csv"
MODEL_PATH = "delay_predictor_model.pkl"
CATEGORICAL_COLUMNS = ["vehicle_type", "weather", "carrier"]
NUMERIC_COLUMNS = ["distance_km", "vendor_rating"]


def load_training_data(path=DATA_PATH):
    """Read the prepared shipment dataset."""
    return pd.read_csv(path)


def build_pipeline():
    """Assemble the preprocessing + model pipeline."""
    encoder_block = ColumnTransformer(
        [("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS)],
        remainder="passthrough",
    )
    return Pipeline(
        [
            ("preprocessor", encoder_block),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
        ]
    )


def evaluate_model(model, features, targets):
    """Return basic regression metrics for inspection."""
    predictions = model.predict(features)
    return {
        "mae": mean_absolute_error(targets, predictions),
        "r2": r2_score(targets, predictions),
    }


def persist_model(model, path=MODEL_PATH):
    joblib.dump(model, path)
    print(f"Model saved as {path}")


def main():
    dataset = load_training_data()
    features = dataset.drop("delay_days", axis=1)
    targets = dataset["delay_days"]

    train_features, test_features, train_targets, test_targets = train_test_split(
        features, targets, test_size=0.2, random_state=42
    )

    pipeline = build_pipeline()
    pipeline.fit(train_features, train_targets)

    train_metrics = evaluate_model(pipeline, train_features, train_targets)
    test_metrics = evaluate_model(pipeline, test_features, test_targets)

    print("Model Performance:")
    print(f"Train MAE: {train_metrics['mae']:.2f}")
    print(f"Test  MAE: {test_metrics['mae']:.2f}")
    print(f"Test  R2 Score: {test_metrics['r2']:.2f}")

    persist_model(pipeline)


if __name__ == "__main__":
    main()
