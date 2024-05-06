import numpy as np

def predict_future_values(model, last_known_features, scaler_feature, scaler_target, N, future_steps, max_actual_value):
    # Use last N known features to start the prediction process
    current_features = last_known_features.copy()
    
    future_predictions = []
    for _ in range(future_steps):
        current_features_scaled = scaler_feature.transform(current_features[-N:])
        current_features_scaled = current_features_scaled.reshape(1, N, -1)
        
        # Predict the next value
        next_prediction_scaled = model.predict(current_features_scaled)
        next_prediction = scaler_target.inverse_transform(next_prediction_scaled).ravel()[0]
        
        # Ensure prediction is non-negative and does not exceed slightly above the maximum actual value
        next_prediction = max(0, min(next_prediction, max_actual_value * 1.05))
        
        # Append the prediction to the list
        future_predictions.append(next_prediction)
        
        # Add the next prediction to the current_features
        next_feature = np.zeros((1, current_features.shape[1]))
        next_feature[:, -1] = next_prediction  # We are assuming the last feature is the predicted feature
        current_features = np.vstack([current_features, next_feature])
    
    return future_predictions


