import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

def train_risk_zone_model():
    """
    Trains a DBSCAN model to find geographical hotspots of incidents and saves the
    trained model to a file.
    """
    print("Starting model training...")

    # --- Step 1: Load the clean data from Phase 1 ---
    df = pd.read_csv("clean_incident_data.csv")
    
    # --- Step 2: Prepare data for DBSCAN ---
    # We only need the latitude and longitude for clustering.
    coords = df[['latitude', 'longitude']].values
    
    # DBSCAN works with distances, so we need to convert lat/lon to a format
    # that represents real-world distance. We convert degrees to radians.
    kms_per_radian = 6371.0088
    epsilon = 0.1 / kms_per_radian # Cluster points within a 100-meter radius

    # --- Step 3: Train the DBSCAN model ---
    # We are looking for clusters of at least 2 incidents.
    db = DBSCAN(eps=epsilon, min_samples=2, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    
    # The `labels_` attribute tells us which cluster each point belongs to.
    # -1 means it's a noisy point (not part of a cluster).
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    
    print(f'Model training complete. Found {num_clusters} high-risk clusters.')

    # --- Step 4: Save the trained model ---
    # We save the model so our API can use it for predictions without retraining.
    joblib.dump(db, 'risk_zone_model.joblib')
    print("Trained model saved to 'risk_zone_model.joblib'")

    # --- Optional: Show the cluster centers ---
    if num_clusters > 0:
        clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
        print("\nHigh-risk zone centers (lat, lon):")
        for cluster in clusters:
            print(cluster.mean(axis=0))

if __name__ == "__main__":
    train_risk_zone_model()