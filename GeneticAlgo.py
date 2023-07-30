import random

# Set up the data
courses = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7']
exam_halls = ['H1', 'H2']
time_slots = ['T1', 'T2', 'T3']

student_conflicts = {
    ('C1', 'C2'): 10,
    ('C1', 'C4'): 5,
    ('C2', 'C5'): 7,
    ('C3', 'C4'): 12,
    ('C4', 'C5'): 8,
    ('C2', 'C6'): 9,
    ('C1', 'C7'): 4
}

hall_hours = {
    'H1': 6,
    'H2': 6
}

# Genetic algorithm parameters
POPULATION_SIZE = 10
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1

def fitness(schedule):
    """
    Calculate the fitness of a schedule as the total number of student conflicts and penalty for exceeding exam hall hours.
    """
    total_conflicts = 0
    total_penalty = 0
    hall_usage = {hall: 0 for hall in exam_halls}
    for pair, num_students in student_conflicts.items():
        c1, c2 = pair
        for (course, time_slot, exam_hall) in schedule:
            if course == c1:
                for (other_course, other_time_slot, other_exam_hall) in schedule:
                    if other_course == c2 and time_slot == other_time_slot:
                        total_conflicts += num_students
            elif course == c2:
                for (other_course, other_time_slot, other_exam_hall) in schedule:
                    if other_course == c1 and time_slot == other_time_slot:
                        total_conflicts += num_students
    for (course, time_slot, exam_hall) in schedule:
        hall_usage[exam_hall] += 1
        if hall_usage[exam_hall] > hall_hours[exam_hall]:
            total_penalty += 10
        for other_course, other_time_slot, other_exam_hall in schedule:
            if (course, other_course) in student_conflicts and time_slot == other_time_slot and exam_hall != other_exam_hall:
                total_penalty += 100
    return -(total_conflicts + total_penalty) # negative value to maximize fitness


def generate_individual():
    """
    Generate a random schedule as an individual.
    """
    schedule = []
    for course in courses:
        time_slot = random.choice(time_slots)
        exam_hall = random.choice(exam_halls)
        schedule.append((course, time_slot, exam_hall))
    return schedule

def generate_new_population(current_population):
    """
    Generate a new population using the current population.
    """
    new_population = []
    while len(new_population) < POPULATION_SIZE:
        # Perform tournament selection with a tournament size of 5
        tournament = random.sample(current_population, 5)
        winner = max(tournament, key=fitness)
        parent1 = winner
        # Choose a second parent randomly from the tournament
        parent2 = random.choice(tournament)
        child = crossover(parent1, parent2)
        if random.uniform(0, 1) <= MUTATION_RATE:
            child = mutate(child)
        new_population.append(child)
    return new_population



def crossover(parent1, parent2):
    """
    Create a new child by performing single-point crossover on the two parents.
    """
    child = []
    for i in range(len(parent1)):
        if random.uniform(0, 1) <= 0.8:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

def mutate(schedule):
    """
    Mutate a schedule by changing the exam hall for a random course.
    """
    course, time_slot, exam_hall = random.choice(schedule)
    new_exam_hall = random.choice(exam_halls)
    while new_exam_hall == exam_hall:
        new_exam_hall = random.choice(exam_halls)
    new_schedule = [(c, t, h) if c != course else (c, t, new_exam_hall) for (c, t, h) in schedule]
    return new_schedule

# Main genetic algorithm loop
current_population = [generate_individual() for i in range(POPULATION_SIZE)]
best_zero_fitness_schedule = None

for i in range(NUM_GENERATIONS):
    print("Generation Number: ", i)
    current_population = sorted(current_population, key=fitness)
    
    for schedule in current_population:
        print(f"Schedule: {schedule}\tFitness score: {fitness(schedule)}")
        
        if fitness(schedule) == 0 and (best_zero_fitness_schedule is None or fitness(schedule) > fitness(best_zero_fitness_schedule)):
            best_zero_fitness_schedule = schedule
            
    if best_zero_fitness_schedule is not None:
        break
    
    current_population = generate_new_population(current_population)
    
# Print the best schedule
if best_zero_fitness_schedule is not None:
    print("Best schedule with minimum conflicts:")
    for course, time_slot, exam_hall in best_zero_fitness_schedule:
        print(f"{course}: {time_slot}, {exam_hall}")
    print(f"Minimum conflicts: 0")
else:
    best_schedule = current_population[0]
    min_conflicts = -fitness(best_schedule)
    
    print("Best schedule with minimum conflicts:")
    for course, time_slot, exam_hall in best_schedule:
        print(f"{course}: {time_slot}, {exam_hall}")
    print(f"Minimum conflicts: {min_conflicts}") 

