#!/usr/bin/env python
# coding: utf-8

import random
import math
import pandas as pd
import logging
from sqlalchemy import create_engine
import pymysql

# Load your dataset from a CSV file
dataset_path = r'C:\Users\Administrator\Downloads\Book1.csv'

df = pd.read_csv(dataset_path)
df['AVE_TEMP'] = pd.to_numeric(df['AVE_TEMP'], errors='coerce')

# Connect to the database using SQLAlchemy
db_connection = create_engine('mysql+pymysql://root:@localhost/esp_data')

# Load the latest avg_AirTemp value from the database
query_latest_temp = "SELECT avg_AirTemp FROM overall_data ORDER BY reading_time DESC LIMIT 1"
latest_temperature_df = pd.read_sql(query_latest_temp, con=db_connection)

# Close the database connection
db_connection.dispose()

# Check if there's data in the dataframe
if not latest_temperature_df.empty:
    # Use the latest temperature value as the input
    current_temperature = float(latest_temperature_df['avg_AirTemp'].iloc[0])
else:
    # If there's no data, set a default value or handle accordingly
    current_temperature = 30.0 

# Genetic Algorithm Parameters
population_size = 50
generations = 100
mutation_rate = 0.1

# Simulated Annealing Parameters
initial_temperature = 150.0
cooling_rate = 0.5

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Check if the temperature is within the optimal range
def calculate_fitness(chromosome, temperature):
    min_temp_threshold = 21
    max_temp_threshold = 32
    chromosome_status = chromosome[0]

    # Check if the temperature is within the optimal range
    if min_temp_threshold <= temperature <= max_temp_threshold:
        if chromosome_status == 'GREEN':
            return 0.0  # High fitness penalty for 'GREEN' status when outside the optimal range
        else:
            return 1.0  # Good fitness for other statuses within the optimal range
    else:
        if chromosome_status == 'RED':
            return 0.0  # Good fitness for 'RED' status when outside the optimal range
        else:
            return 1.0  # High fitness penalty for other statuses when outside the optimal range

    
# Genetic Algorithm
def genetic_algorithm():
    global initial_temperature  # Declare initial_temperature as a global variable
    initial_temperature = 100.0

    population = [
        (random.choice(df['STATUS'].unique()),) for _ in range(population_size)]

    fitness_history = []

    for generation in range(generations):
        fitness_scores = [calculate_fitness(chromosome, current_temperature) for chromosome in population]

        selected_indices = random.choices(
            range(population_size), weights=[1 / (fitness + 1e-10) for fitness in fitness_scores], k=population_size
        )

        offspring = crossover_and_mutation(population, selected_indices)

        population = apply_simulated_annealing(population, fitness_scores, offspring)

        best_solution = population[min(range(population_size), key=lambda i: fitness_scores[i])]
        logging.info(f"Generation {generation + 1}: Best solution - {best_solution}, Fitness - {calculate_fitness(best_solution, current_temperature)}")

        fitness_history.append(min(fitness_scores))

    # Plot fitness convergence
    # (Note: Matplotlib plotting may not work in certain web server environments)
    # plt.plot(fitness_history)
    # plt.xlabel('Generation')
    # plt.ylabel('Fitness')
    # plt.title('Fitness Convergence')
    # plt.show()

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
    global initial_temperature  # Declare initial_temperature as a global variable
    for i in range(population_size):
        current_fitness = fitness_scores[i]
        candidate_solution = offspring[i]
        candidate_fitness = calculate_fitness(candidate_solution, current_temperature)

        if candidate_fitness < current_fitness or random.random() < math.exp(
            (current_fitness - candidate_fitness) / initial_temperature
        ):
            population[i] = candidate_solution

    # Cooling
    initial_temperature *= cooling_rate

    return population

# Example usage
final_population = genetic_algorithm()
best_solution = final_population[min(range(population_size), key=lambda i: calculate_fitness(final_population[i], current_temperature))]

# Assuming 'actual_status' is the actual STATUS in your dataset
actual_status = df['STATUS'].tolist()

# Assuming 'predicted_status' is the predicted STATUS from the best solution
predicted_status = [best_solution[0]] * len(actual_status)

# Print the lengths of both lists for troubleshooting
print("Length of actual_status:", len(actual_status))
print("Length of predicted_status:", len(predicted_status))

# Calculate accuracy
correct_predictions = sum(actual_status[i] == predicted_status[i] for i in range(len(actual_status)))
total_predictions = len(actual_status)
accuracy = correct_predictions / total_predictions * 100

print(f"Accuracy: {accuracy:.2f}%")
print("Best solution:", best_solution)
