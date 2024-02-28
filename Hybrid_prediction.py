import random
import math
import pandas as pd
import logging
# from sqlalchemy import create_engine
# import pymysql
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

min_temp_value = 21.0
max_temp_value = 32.0
min_soil_temp_value = 15.0
max_soil_temp_value = 35.0  # Replace with the actual max value
min_nitrogen_value = 120.0
max_nitrogen_value = 180.0  # Replace with the actual max value
min_phosphorous_value = 60.0
max_phosphorous_value = 100.0  # Replace with the actual max value
min_potassium_value = 90.0
max_potassium_value = 150.0  # Replace with the actual max value
min_solar_rad_value = 15.0
max_solar_rad_value = 25.0
min_rainfall_value = 0.0
max_rainfall_value = 3.0

def normalize_value(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value) if (max_value - min_value) != 0 else 0

# Update your calculate_fitness function to use normalized values
def calculate_fitness(chromosome, temperature, soil_temp, nitrogen, phosphorous, potassium, solar_rad, rainfall):
    chromosome_status = chromosome[0]

    # Normalize the features
    normalized_temperature = normalize_value(temperature, min_temp_value, max_temp_value)
    normalized_soil_temp = normalize_value(soil_temp, min_soil_temp_value, max_soil_temp_value)
    normalized_nitrogen = normalize_value(nitrogen, min_nitrogen_value, max_nitrogen_value)
    normalized_phosphorous = normalize_value(phosphorous, min_phosphorous_value, max_phosphorous_value)
    normalized_potassium = normalize_value(potassium, min_potassium_value, max_potassium_value)
    normalized_solar_rad = normalize_value(solar_rad, min_solar_rad_value, max_solar_rad_value)
    normalized_rainfall = normalize_value(rainfall, min_rainfall_value, max_rainfall_value)

    if (
        0 <= normalized_temperature <= 1
        and 0 <= normalized_soil_temp <= 1
        and 0 <= normalized_nitrogen <= 1
        and 0 <= normalized_phosphorous <= 1
        and 0 <= normalized_potassium <= 1
        and 0 <= normalized_solar_rad <= 1
        and 0 <= normalized_rainfall <= 1
    ):
        # Adjust thresholds accordingly based on normalized values
        if chromosome_status == 'GREEN':
            return 0.0
        elif chromosome_status == 'YELLOW':
            return 1.0
        else:
            return 2.0
    else:
        if chromosome_status == 'RED':
            return 0.0
        elif chromosome_status == 'YELLOW':
            return 1.0
        else:
            return 2.0

dataset_path = 'C:/xampp/htdocs/final/TEST.csv'
df = pd.read_csv(dataset_path)
df['AVE_TEMP'] = pd.to_numeric(df['AVE_TEMP'], errors='coerce')

try:
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='esp_data',
        time_zone='+8:00'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Access denied. Check your username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist.")
    else:
        print(f"Error: {err}")
    exit()
# Get the current date from the database
query_current_date = "SELECT CURDATE()"
cursor_date = db_connection.cursor()
cursor_date.execute(query_current_date)
current_date_result = cursor_date.fetchone()
cursor_date.close()

current_date = current_date_result[0] if current_date_result else "N/A"
print(f"Fetched data from the database on: {current_date}")
query_latest_temp = f"SELECT AVG(all_air_temp) FROM overall_data WHERE reading_date = '{current_date}'"
query_latest_soil_temp = f"SELECT AVG(all_soil_temperature) FROM overall_data WHERE reading_date = '{current_date}'"
query_latest_n = f"SELECT AVG(all_nitrogen) FROM overall_data WHERE reading_date = '{current_date}'"
query_latest_p = f"SELECT AVG(all_phosphorus) FROM overall_data WHERE reading_date = '{current_date}'"
query_latest_k = f"SELECT AVG(all_potassium) FROM overall_data WHERE reading_date = '{current_date}'"
current_solar_rad = float(df['SOLAR_RAD'].iloc[0]) if not df.empty else 0.0
current_rainfall = float(df['RAINFALL'].iloc[0]) if not df.empty else 0.0


def execute_query(query, current_date):
    cursor = db_connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    print(f"Fetched data from the database on: {current_date}")

    return float(result[0]) if result and cursor.rowcount > 0 else 0.0

current_temperature = execute_query(query_latest_temp, current_date)
current_soil_temp = execute_query(query_latest_soil_temp, current_date)
current_nitrogen = execute_query(query_latest_n, current_date)
current_phosphorous = execute_query(query_latest_p, current_date)
current_potassium = execute_query(query_latest_k, current_date)

# Print the fetched values
print("Fetched values from the database:")
print(f"Current Date: {current_date}")
print(f"Current Temperature: {current_temperature}")
print(f"Current Soil Temperature: {current_soil_temp}")
print(f"Current Nitrogen: {current_nitrogen}")
print(f"Current Phosphorous: {current_phosphorous}")
print(f"Current Potassium: {current_potassium}")

current_temperature = execute_query(query_latest_temp, current_date)
current_soil_temp = execute_query(query_latest_soil_temp, current_date)
current_nitrogen = execute_query(query_latest_n, current_date)
current_phosphorous = execute_query(query_latest_p, current_date)
current_potassium = execute_query(query_latest_k, current_date)
current_solar_rad = float(df['SOLAR_RAD'].iloc[0]) if not df.empty else 0.0
current_rainfall = float(df['RAINFALL'].iloc[0]) if not df.empty else 0.0

db_connection.close()

# Genetic Algorithm Parameters
population_size = 50
generations = 100
mutation_rate = 0.1

# Simulated Annealing Parameters
initial_temperature = 150.0
cooling_rate = 0.5

# Logging configuration
logging.basicConfig(level=logging.INFO)

def genetic_algorithm():
    global initial_temperature
    initial_temperature = 100.0

    population = [
        (random.choice(df['STATUS'].unique()),) for _ in range(population_size)]

    fitness_history = []

    for generation in range(generations):
        fitness_scores = [calculate_fitness(chromosome, current_temperature, current_soil_temp,
                                    current_nitrogen, current_phosphorous, current_potassium,
                                    current_solar_rad, current_rainfall) for chromosome in population]


        selected_indices = random.choices(
            range(population_size), weights=[1 / (fitness + 1e-10) for fitness in fitness_scores], k=population_size
        )

        offspring = crossover_and_mutation(population, selected_indices)

        population = apply_simulated_annealing(
            population, fitness_scores, offspring)

        best_solution = population[min(
            range(population_size), key=lambda i: fitness_scores[i])]
        logging.info(
            f"Generation {generation + 1}: Best solution - {best_solution}, Fitness - {calculate_fitness(best_solution, current_temperature, current_soil_temp, current_nitrogen, current_phosphorous, current_potassium, current_solar_rad, current_rainfall)}")

        fitness_history.append(min(fitness_scores))

    return population

def crossover_and_mutation(population, selected_indices):
    offspring = []
    for i in range(0, population_size, 2):
        parent1 = population[selected_indices[i]]
        parent2 = population[selected_indices[i + 1]]
        crossover_point = random.randint(0, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        offspring.extend([child1, child2])

    for i in range(population_size):
        if random.random() < mutation_rate:
            mutated_chromosome = list(offspring[i])
            mutated_chromosome[0] = random.choice(df['STATUS'].unique())
            offspring[i] = tuple(mutated_chromosome)

    return offspring

def apply_simulated_annealing(population, fitness_scores, offspring):
    global initial_temperature
    for i in range(population_size):
        current_fitness = fitness_scores[i]
        candidate_solution = offspring[i]
        candidate_fitness = calculate_fitness(candidate_solution, current_temperature,
                                      current_soil_temp, current_nitrogen, current_phosphorous,
                                      current_potassium, current_solar_rad, current_rainfall)

        if candidate_fitness < current_fitness or random.random() < math.exp(
            (current_fitness - candidate_fitness) / initial_temperature
        ):
            population[i] = candidate_solution

    initial_temperature *= cooling_rate

    return population

final_population = genetic_algorithm()
best_solution = final_population[min(
    range(population_size), key=lambda i: calculate_fitness(final_population[i], current_temperature,
                                                             current_soil_temp, current_nitrogen,
                                                             current_phosphorous, current_potassium,
                                                             current_solar_rad, current_rainfall))]

actual_status = df['STATUS'].tolist()

predicted_status = [best_solution[0]] * len(actual_status)

print("Length of actual_status:", len(actual_status))
print("Length of predicted_status:", len(predicted_status))

correct_predictions = sum(
    actual_status[i] == predicted_status[i] for i in range(len(actual_status)))
total_predictions = len(actual_status)
accuracy = correct_predictions / total_predictions * 100

print(f"Accuracy: {accuracy:.2f}%")
print("Best solution:", best_solution)
# # Execute the update query based on the predicted status
# update_query = f"UPDATE overall_data SET hybrid_status = {1 if best_solution[0] == 'GREEN' else 0} WHERE reading_date = '{current_date}'"
# # Convert the predicted status to 1 for 'green' and 0 otherwise
# predicted_status_value = 1 if best_solution[0] == 'GREEN' else 0

formatted_current_date = datetime.now().strftime('%Y-%m-%d')

# print("Predicted Status:", predicted_status)
print("Date of Adjustment:", formatted_current_date)


# Update the hybrid_status column in the database
update_query = f"""
    UPDATE overall_data
    SET hybrid_status = %s
    WHERE reading_date = %s
"""

try:
    # Reopen the MySQL connection
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='esp_data',
        time_zone='+8:00'
    )

    update_cursor = db_connection.cursor()

    # Map the predicted_status_value to the corresponding string value
    if best_solution[0] == 'GREEN':
        predicted_status_value = 'Green'
    elif best_solution[0] == 'YELLOW':
        predicted_status_value = 'Yellow'
    else:
        predicted_status_value = 'Red'

    update_cursor.execute(update_query, (predicted_status_value, formatted_current_date))
    db_connection.commit()  # Commit the changes
    print("Update successful.")
except Exception as e:
    print("Error during update:", e)
finally:
    if 'db_connection' in locals() and db_connection.is_connected():
        update_cursor.close()  # Close the cursor
        db_connection.close()  # Close the connection
