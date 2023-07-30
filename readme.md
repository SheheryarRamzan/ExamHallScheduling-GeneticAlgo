# Code Overview 
This code implements a genetic algorithm to generate a schedule for a set of courses in which each 
course is assigned a time slot and an exam hall. The goal is to minimize the number of student conflicts 
and the penalty for exceeding exam hall hours or having conflicting exams in the same time slot.
The main steps of the algorithm are:
1. Generate an initial population of random schedules.
2. Evaluate the fitness of each schedule based on the number of student conflicts and penalty.
3. Select the best schedules using tournament selection.
4. Create new offspring schedules by performing single-point crossover and mutation.
5. Replace the old population with the new population and repeat steps 2-4 until a satisfactory 
solution is found or the maximum number of generations is reached.
The fitness function calculates the total number of student conflicts and penalty for each schedule. It 
iterates over all pairs of conflicting courses and checks if they are scheduled in the same time slot and 
exam hall. It also checks if a course exceeds the allowed exam hall hours and if there are any conflicting 
exams in the same time slot but different exam halls.
The code prints the best schedule found and its fitness score at each generation. If a schedule with zero 
conflicts is found, it is immediately returned as the best solution. Otherwise, the algorithm terminates 
after the specified number of generations.
