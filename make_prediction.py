import sys
import joblib
import pandas as pd

# Load the pre-trained model
model = joblib.load('crop_season_predictor_model.pkl')

# Function to make predictions
def make_prediction(avg_air_temp):
    # Use placeholder values for 'year', 'month', and 'day'
    input_data = {
        'year': 2020,  # Placeholder
        'month': 1,    # Placeholder
        'day': 1,      # Placeholder
        'avg_AirTemp': avg_air_temp
    }

    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Make a prediction
    prediction = model.predict(input_df)
    return prediction[0]

if __name__ == "__main__":
    # Take the average air temperature as command-line argument
    avg_air_temp = float(sys.argv[1])
    result = make_prediction(avg_air_temp)
    print(result)
