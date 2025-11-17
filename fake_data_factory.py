import random

import pandas as pd


WEATHER_STATES = ["Sunny", "Rain", "Storm", "Fog"]
VEHICLE_TYPES = ["Truck", "Van", "Bike"]
CARRIERS = ["Blue Dart", "Delhivery", "FedEx", "DTDC"]
OUTPUT_PATH = "shipment_data.csv"


def _simulate_delay(route_distance, weather_condition, transport_mode, supplier_rating):
    baseline = route_distance / 800
    weather_penalties = {"Storm": 2, "Rain": 1, "Fog": 1.5}
    vehicle_penalties = {"Bike": 0.5, "Truck": 1}

    baseline += weather_penalties.get(weather_condition, 0)
    baseline += vehicle_penalties.get(transport_mode, 0)
    baseline += (5 - supplier_rating) * 0.3

    jitter = random.uniform(-0.5, 0.5)
    return max(0, round(baseline + jitter, 2))


def create_synthetic_data(sample_count=500):
    rows = []
    for _ in range(sample_count):
        route_distance = random.randint(50, 2000)
        transport_mode = random.choice(VEHICLE_TYPES)
        supplier_rating = random.randint(1, 5)
        weather_condition = random.choice(WEATHER_STATES)

        delay_duration = _simulate_delay(
            route_distance, weather_condition, transport_mode, supplier_rating
        )
        carrier_name = random.choice(CARRIERS)

        rows.append(
            [
                route_distance,
                transport_mode,
                supplier_rating,
                weather_condition,
                carrier_name,
                delay_duration,
            ]
        )

    df = pd.DataFrame(
        rows, columns=["distance_km", "vehicle_type", "vendor_rating", "weather", "carrier", "delay_days"]
    )
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Synthetic data saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_synthetic_data()