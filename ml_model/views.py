from django.shortcuts import render
import numpy as np
import pandas as pd
from keras.models import load_model

# Create your views here.


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

# Load the best model
best_model_path = 'best_model.h5'
best_model = load_model(best_model_path)

# Determine the maximum value from the actuals to set as the upper limit for predictions
max_actual_value = df['Generation'].max()

# Predict future power generation
future_steps = 7  # Define how many days to predict into the future
feature_columns = [col for col in df.columns if col not in ['Generation']]  # Exclude the target variable
last_known_features = df[feature_columns].iloc[-N:].values  # Get the last N known values

# Generate predictions and clip them to the desired range
# Generate predictions using the predict_future_values function
future_power_generation = predict_future_values(
    best_model, last_known_features, scaler_feature, scaler_target, N, future_steps, max_actual_value)

# Convert future dates to a datetime index
last_date = df.index[-1]
future_dates = pd.date_range(start=last_date, periods=future_steps + 1, freq='D')[1:]

# Plotting only the future predictions
plt.figure(figsize=(15, 7))
plt.plot(future_dates, future_power_generation, 'r--', label='Predicted Future Power Generation')

# Formatting the X-axis to show each date
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()  # Rotation to prevent overlap

# Setting Y-axis limits
plt.ylim(0, max(future_power_generation))  # Set the Y-axis to only go up to the max of the predictions

plt.title('Predicted Future Power Generation')
plt.xlabel('Date')
plt.ylabel('Power Generation')
plt.legend()
plt.show()