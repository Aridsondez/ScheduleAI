import pandas as pd
import random
import json

def generate_sample_data(num_samples = 5):
    employee_names = ["Alice", "Bob", "Aridsondez", "Jerome", "Daniel"]

    data = []

    for i in range(num_samples):
        name = random.choice(employee_names)
        efficiency = random.randint(50, 100)
        availability = generate_random_availability()
        relationships = generate_random_relationships(employee_names)

        data.append({
            "name": name,
            "efficiency": efficiency,
            "availability" : json.dumps(availability),
            "relationships" : json.dumps(relationships)
        })

        df = pd.DataFrame(data)
        df.to_csv('employee_data.csv', index = False)

def generate_random_availability():
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Satuday","Sunday"]
    availability = {}

    for day in days_of_week:
        if random.choice([True, False]):
            num_slots = random.randint(1, 3)  # Randomly decide how many shifts they have in a day
            time_slots = []
            available_hours = 6  # Starting from 6 AM
            
            for _ in range(num_slots):
                # Define a start hour that is at least after the last end time
                start_hour = available_hours
                end_hour = min(start_hour + random.randint(1, 4), 22)  # End time can be between 1 and 4 hours after start, but no later than 10 PM
                
                time_slots.append(f"{start_hour}:00 - {end_hour}:00")
                
                # Update available_hours to start after the current shift ends
                available_hours = end_hour
            
            availability[day] = time_slots
    return availability


def generate_random_relationships(employee_names):
    relationships = {}

    for employees in employee_names:
        relationships[employees]= random.randint(0, 10)
    return relationships


generate_sample_data(4)