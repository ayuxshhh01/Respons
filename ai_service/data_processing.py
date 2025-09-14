import pandas as pd

def process_raw_data():
    """
    This function simulates cleaning and structuring raw data from various sources
    into a unified format for model training. This represents the "historical crime,
    accident, missing cases, and seasonal data".
    """
    print("Starting data processing...")
    
    # --- Step 1: Simulate Raw Data Sources ---
    # In a real project, this would be loaded from CSVs, police reports, etc.
    mock_crime_data = [
        {"date": "2024-01-15", "location_desc": "Near Siddheshwar Temple, Solapur", "type": "theft"},
        {"date": "2024-03-22", "location_desc": "Bhuikot Fort, Solapur", "type": "assault"},
        {"date": "2024-04-05", "location_desc": "Near Siddheshwar Temple, Solapur", "type": "theft"},
    ]
    
    mock_accident_data = [
        {"timestamp": "2024-02-10 18:30:00", "area": "Pune-Solapur Highway near Pakni", "severity": "minor"},
    ]

    # --- Step 2: Simulate Geocoding ---
    # In a real project, use a service like GeoPy to convert addresses to coordinates.
    geocoded_locations = {
        "Near Siddheshwar Temple, Solapur": {"lat": 17.672, "lon": 75.923},
        "Bhuikot Fort, Solapur": {"lat": 17.668, "lon": 75.911},
        "Pune-Solapur Highway near Pakni": {"lat": 17.701, "lon": 75.855},
    }

    processed_data = []

    # --- Step 3: Clean and Unify Data ---
    for record in mock_crime_data:
        loc = geocoded_locations.get(record["location_desc"])
        if loc:
            processed_data.append({
                "timestamp": pd.to_datetime(record["date"]),
                "latitude": loc["lat"],
                "longitude": loc["lon"],
                "event_type": "crime",
            })

    for record in mock_accident_data:
        loc = geocoded_locations.get(record["area"])
        if loc:
             processed_data.append({
                "timestamp": pd.to_datetime(record["timestamp"]),
                "latitude": loc["lat"],
                "longitude": loc["lon"],
                "event_type": "accident",
            })

    # Create a pandas DataFrame
    df = pd.DataFrame(processed_data)
    
    # --- Step 4: Save the Clean Data ---
    # This clean file is the input for our model training phase.
    df.to_csv("clean_incident_data.csv", index=False)
    
    print("Data processing complete. Clean data saved to 'clean_incident_data.csv'")
    print("\nSample of clean data:")
    print(df.head())

if __name__ == "__main__":
    process_raw_data()