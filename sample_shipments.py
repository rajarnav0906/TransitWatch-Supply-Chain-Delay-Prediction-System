def fetch_shipments():
    """Quick helper to stub out a shipment list for UI demos."""
    return [
        {
            "id": "SHP001",
            "origin": "Delhi",
            "destination": "Mumbai",
            "status": "In Transit",
            "eta": "2025-07-10",
        },
        {
            "id": "SHP002",
            "origin": "Bangalore",
            "destination": "Chennai",
            "status": "Delayed",
            "eta": "2025-07-08",
        },
    ]
