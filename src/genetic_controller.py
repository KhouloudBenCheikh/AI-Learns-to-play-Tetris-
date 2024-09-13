from os import pardir  # Import for navigating file paths
import numpy as np  # Import for numerical operations
from game import Game  # Import the Game class
from genetic import Genetic_AI  # Import the Genetic_AI class
import random  # Import for random number generation
import pandas as pd  # Import for data manipulation and saving to CSV

def cross(a1, a2, aggregate="lin"):
    """
    Create a new agent by combining traits of two parent agents.
    """
    new_genotype = []  # List to store the new agent's genotype
    a1_prop = a1.fit_rel / a2.fit_rel  # Calculate relative fitness ratio
    
    for i in range(len(a1.genotype)):
        rand = random.uniform(0, 1)  # Generate a random number between 0 and 1
        if rand > a1_prop:
            new_genotype.append(a1.genotype[i])  # Add trait from the first parent
        else:
            new_genotype.append(a2.genotype[i])  # Add trait from the second parent

    # Create and return a new Genetic_AI agent with the new genotype
    return Genetic_AI(genotype=np.array(new_genotype), aggregate=aggregate, mutate=True)

def compute_fitness(agent, num_trials):
    """
    Evaluate the agent's performance over a number of trials.
    """
    fitness = []  # List to store fitness scores from each trial
    
    for _ in range(num_trials):
        game = Game('genetic', agent=agent)  # Create a new game with the agent
        peices_dropped, rows_cleared = game.run_no_visual()  # Run the game and get performance metrics
        fitness.append(peices_dropped)  # Add the number of pieces dropped to the list
        print(f"    Trial: {_}/{num_trials}")  # Print progress

    # Return the average fitness score
    return np.average(np.array(fitness))

def run_X_epochs(num_epochs=10, num_trials=5, pop_size=100, aggregate='lin', num_elite=5, survival_rate=.35, logging_file='default.csv'):
    """
    Run the genetic algorithm for a given number of epochs.
    """
    # Initialize data collection
    data=[[1, np.ones(9), 1, np.ones(9), 1, np.ones(9)]]
    headers = ['avg_fit','avg_gene', 'top_fit', 'top_gene', 'elite_fit', 'elite_gene']
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(f'data/{logging_file}.csv', index=False)  # Save initial data to CSV

    # Create the initial population of agents
    population = [Genetic_AI(aggregate=aggregate) for _ in range(pop_size)]

    for epoch in range(num_epochs):
        """
        Evaluate fitness of each agent.
        """
        total_fitness = 0  # Total fitness of the population
        top_agent = 0  # The agent with the highest fitness
        gene = np.zeros(9)  # Placeholder for cumulative genotype

        for n in range(pop_size):
            print(f"Agent: {n}/{pop_size}")  # Print progress
            agent = population[n]
            agent.fit_score = compute_fitness(agent, num_trials=num_trials)  # Compute fitness
            total_fitness += agent.fit_score  # Update total fitness
            gene += agent.genotype  # Accumulate genotypes

        # Calculate the relative fitness of each agent
        for agent in population:
            agent.fit_rel = agent.fit_score / total_fitness

        """
        Selection and reproduction.
        """
        next_gen = []  # List to store the next generation of agents

        # Sort agents by fitness in descending order
        sorted_pop = sorted(population, reverse=True)

        # Select elite agents and add them to the next generation
        elite_fit_score = 0
        elite_genes = np.zeros(9)
        top_agent = sorted_pop[0]

        for i in range(num_elite):
            elite_fit_score += sorted_pop[i].fit_score
            elite_genes += sorted_pop[i].genotype
            next_gen.append(Genetic_AI(genotype=sorted_pop[i].genotype, mutate=False))

        # Select parents based on survival rate
        num_parents = round(pop_size * survival_rate)
        parents = sorted_pop[:num_parents]

        # Create new agents by crossing over genotypes of randomly chosen parents
        for _ in range(pop_size - num_elite):
            # Randomly select two parents and perform crossover
            parents = random.sample(parents, 2)
            next_gen.append(cross(parents[0], parents[1], aggregate=aggregate))

        # Calculate and save statistics for the current epoch
        avg_fit = (total_fitness / pop_size)
        avg_gene = (gene / pop_size)
        top_fit = (top_agent.fit_score)
        top_gene = (top_agent.genotype)
        elite_fit = (elite_fit_score / num_elite)
        elite_gene = (elite_genes / num_elite)

        data = [[avg_fit, avg_gene, top_fit, top_gene, elite_fit, elite_gene]]
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(f'data/{logging_file}.csv', mode='a', index=False, header=False)

        print(f'\nEpoch {epoch}: \n    total fitness: {total_fitness/pop_size}\n    best agent: {top_agent.fit_score}\n')

        population = next_gen  # Set the population for the next epoch

    return data

if __name__ == '__main__':
    run_X_epochs(num_epochs=15, num_trials=5, pop_size=50, num_elite=5)
