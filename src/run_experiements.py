from genetic_controller import run_X_epochs

def run_genetic_experiments():
    """
    Runs genetic algorithm experiments with varying population sizes.
    Each experiment runs for a specified number of epochs and trials.
    Results are saved to different logging files based on population size.
    """
    population_sizes = [8, 10, 15]
    num_epochs = 5
    num_trials = 2
    survival_rate = 0.2
    num_elite = 2

    for pop_size in population_sizes:
        logging_file = f'genetic/data_{pop_size}'
        run_X_epochs(
            num_epochs=num_epochs,
            num_trials=num_trials,
            pop_size=pop_size,
            survival_rate=survival_rate,
            num_elite=num_elite,
            logging_file=logging_file
        )

if __name__ == '__main__':
    run_genetic_experiments()
