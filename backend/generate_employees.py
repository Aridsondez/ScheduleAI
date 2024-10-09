import pandas as pd
import random
import json
from flask import request

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
                start_hour = min(available_hours + random.randint(0,12),18)
                end_hour = min(start_hour + random.randint(1, 4), 22)  # End time can be between 1 and 4 hours after start, but no later than 10 PM
                
                time_slots.append(f"{start_hour}:00 - {end_hour}:00")
                
                # Update available_hours to start after the current shift ends
                available_hours = end_hour
            
            availability[day] = parse_availibility( time_slots)
    return availability


def generate_random_relationships(employee_names):
    relationships = {}

    for employees in employee_names:
        relationships[employees]= random.randint(0, 10)
    return relationships


def parse_availibility(time_slots):
    if not time_slots:
        return []
    parsed_slots = []

    for slot in time_slots:
        start_time, end_time = slot.split(" - ")
        start_hour = int (start_time.split(":")[0])
        end_hour = int (end_time.split(":")[0])
        parsed_slots.append((start_hour,end_hour))

    parsed_slots.sort()

    # Merge overlapping or consecutive time slots
    merged_slots = [parsed_slots[0]]
    for current_slot in parsed_slots[1:]:
        last_merged_slot = merged_slots[-1]

        if current_slot[0] <= last_merged_slot[1]:  # If overlapping or consecutive
            # Merge the slots by extending the end time
            merged_slots[-1] = (last_merged_slot[0], max(last_merged_slot[1], current_slot[1]))
        else:
            # Add a new time slot if no overlap
            merged_slots.append(current_slot)

    # Convert merged slots back to "start_hour:end_hour" format
    formatted_slots = [f"{start}:00 - {end}:00" for start, end in merged_slots]

    return formatted_slots


def send_employees_to_backend():
    with open('employee_data.csv') as f:
        df = pd.read_csv(f)
        employee_list = df.to_dict(oreint = 'records')
    response = request.post("http://localhost:5000/add_employees", json=employee_list)
    print(response.json())


generate_sample_data(4)
