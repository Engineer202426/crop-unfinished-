import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import mysql.connector
from datetime import datetime

current_date = datetime.now().strftime('%d/%m/%Y')

# Connect to the MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='esp_data'
)

cursor = connection.cursor()

# Assuming you have a CSV file named 'your_dataset.csv'
dataset_path = 'C:/xampp/htdocs/crop/TEST.csv'
df = pd.read_csv(dataset_path)

df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y', errors='coerce')

label_encoder = LabelEncoder()
df['STATUS'] = label_encoder.fit_transform(df['STATUS'])

# Include 'SOLAR_RAD' and 'RAINFALL' in the feature set
numeric_cols = ['AVE_TEMP', 'SOIL_TEMP', 'N', 'P', 'K', 'SOLAR_RAD', 'RAINFALL']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing target variable 'STATUS'
df = df.dropna(subset=['STATUS'])

X = df[numeric_cols]
y = df['STATUS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", classification_rep)

# Save the model to a file
model_filename = 'Machine_Learning.pkl'
joblib.dump(model, model_filename)

print(f"Model saved to {model_filename}")
#END OF MACHINE LEARNING CODES...

#DATABASE CONNECTION...
# Sensor Reading
current_date_str = datetime.now().strftime('%Y-%m-%d')

sample_temperature_query = f"SELECT all_air_temp FROM overall_data WHERE reading_date = '{current_date_str}' ORDER BY reading_date DESC LIMIT 1"
sample_soil_temp_query = f"SELECT all_soil_temperature FROM overall_data WHERE reading_date = '{current_date_str}' ORDER BY reading_date DESC LIMIT 1"
sample_n_query = f"SELECT all_nitrogen FROM overall_data WHERE reading_date = '{current_date_str}' ORDER BY reading_date DESC LIMIT 1"
sample_p_query = f"SELECT all_phosphorus FROM overall_data WHERE reading_date = '{current_date_str}' ORDER BY reading_date DESC LIMIT 1"
sample_k_query = f"SELECT all_potassium FROM overall_data WHERE reading_date = '{current_date_str}' ORDER BY reading_date DESC LIMIT 1"

# Execute queries to get the latest sensor readings
cursor.execute(sample_temperature_query)
sample_temperature_result = cursor.fetchone()
sample_temperature = float(sample_temperature_result[0]) if sample_temperature_result and cursor.rowcount > 0 else 33.0

cursor.execute(sample_soil_temp_query)
sample_soil_temp_result = cursor.fetchone()
sample_soil_temp = float(sample_soil_temp_result[0]) if sample_soil_temp_result and cursor.rowcount > 0 else 90

cursor.execute(sample_n_query)
sample_n_result = cursor.fetchone()
sample_n = float(sample_n_result[0]) if sample_n_result and cursor.rowcount > 0 else 32

cursor.execute(sample_p_query)
sample_p_result = cursor.fetchone()
sample_p = float(sample_p_result[0]) if sample_p_result and cursor.rowcount > 0 else 42

cursor.execute(sample_k_query)
sample_k_result = cursor.fetchone()
sample_k = float(sample_k_result[0]) if sample_k_result and cursor.rowcount > 0 else 11

sample_solar_rad = df['SOLAR_RAD'].median()  # Use the median value from the dataset
sample_rainfall = df['RAINFALL'].median()  # Use the median value from the dataset

sample_values = {'AVE_TEMP': sample_temperature,
                 'SOIL_TEMP': sample_soil_temp,
                 'N': sample_n,
                 'P': sample_p,
                 'K': sample_k,
                 'SOLAR_RAD': sample_solar_rad,
                 'RAINFALL': sample_rainfall}

sample_values['DATE'] = current_date
sample_df = pd.DataFrame([sample_values], columns=['AVE_TEMP', 'SOIL_TEMP', 'N', 'P', 'K', 'SOLAR_RAD', 'RAINFALL', 'reading_date'])

sample_df['DATE'] = pd.to_datetime(sample_df['reading_date'], format='%d/%m/%Y', errors='coerce')

# Extract features for prediction

print("Values used for prediction:")
for col, value in sample_values.items():
    print(f"{col}: {value}")

features_for_prediction = numeric_cols  # Exclude 'reading_date'

sample_data_for_prediction = sample_df[numeric_cols]

# Load the model from the file
loaded_model = joblib.load(model_filename)

sample_prediction = loaded_model.predict(sample_data_for_prediction)

predicted_status = label_encoder.inverse_transform(sample_prediction)

print("Prediction:", predicted_status[0])

# Use the predicted status directly for updating the database
predicted_status_value = predicted_status[0]

formatted_current_date = datetime.now().strftime('%Y-%m-%d')

print("Predicted Status:", predicted_status)
print("Date of Adjustment:", formatted_current_date)

update_query = """
    UPDATE overall_data
    SET status = %s
    WHERE reading_date = %s
"""

# Try executing the update query with error handling
update_cursor = connection.cursor()
try:
    update_cursor.execute(update_query, (predicted_status_value, formatted_current_date))
    connection.commit()  # Commit the changes
    print("Update successful.")
except Exception as e:
    print("Error during update:", e)
finally:
    update_cursor.close()  # Close the cursor

# Close the database connection
connection.close()
