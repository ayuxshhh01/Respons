import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# --- 1. Initialize the FastAPI Application ---
app = FastAPI(
    title="Smart Tourist Safety AI Service",
    description="Provides predictions for risk zones and other anomalies.",
    version="1.0.0",
)

# --- 2. Load the Trained Model and Data ---
# The model and data are loaded once when the API starts up.
try:
    risk_model = joblib.load("risk_zone_model.joblib")
    incident_data = pd.read_csv("clean_incident_data.csv")
    print("AI model and incident data loaded successfully.")
except FileNotFoundError:
    risk_model = None
    incident_data = None
    print("Warning: Model or data file not found. API will run with mock data.")

# --- 3. Define Data Models for API Requests ---
# These models ensure that the data sent to your API is in the correct format.
class GpsPoint(BaseModel):
    lat: float
    lon: float

class Route(BaseModel):
    points: List[GpsPoint]

# --- 4. Pre-calculate Cluster Centers ---
# We calculate the centers of the high-risk zones once to serve them quickly.
cluster_centers = []
if risk_model and incident_data is not None:
    labels = risk_model.labels_
    unique_labels = set(labels)
    coords = incident_data[['latitude', 'longitude']].values
    
    for label in unique_labels:
        if label != -1: # -1 represents noise points, not a cluster
            cluster_points = coords[labels == label]
            center = cluster_points.mean(axis=0)
            cluster_centers.append({"lat": center[0], "lon": center[1], "risk_level": "High"})

# --- 5. Define the API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "AI Service is running. Navigate to /docs for the API interface."}

@app.post("/predict-risk-zones")
def predict_risk_zones():
    """
    Returns the pre-calculated centers of all high-risk incident zones.
    This endpoint powers the "Heatmaps of ... predicted danger zones".
    """
    if not cluster_centers:
         return {"warning": "No clusters found in the model or model not loaded.", "predicted_hotspots": []}
         
    print(f"Returning {len(cluster_centers)} pre-calculated high-risk zones.")
    return {"predicted_hotspots": cluster_centers}

@app.post("/check-route-anomaly")
def check_route_anomaly(route: Route):
    """
    Simulates the "AI Anomaly Detection" for unusual routes.
    In a real system, this would use a trained LSTM model.
    """
    print(f"Checking route with {len(route.points)} points for anomalies.")
    # Simple mock logic: A route is anomalous if it has more than 10 waypoints
    # or if its total length is unusually long.
    is_anomaly = len(route.points) > 10
    
    return {
        "is_anomaly": is_anomaly,
        "message": "Potential route deviation detected." if is_anomaly else "Route appears normal."
    }