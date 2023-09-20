import neat
#import matplotlib.pyplot as plt
import pickle
#import threading
#import visualize
from game import Game
from functools import partial


#most of the commented out code is used for plotting / debugging
#uncomment for visualizing
#it also causes a bug which resizes the pygame window for some reason
#seems to be an issue with the pygame window losing focus while plot shows

# x_data = []
# y_data = []


# def update_plot():
#     plt.ion()
#     fig, ax = plt.subplots()
    
#     while True:
#         ax.clear()
#         ax.set_xlabel('Generation')
#         ax.set_ylabel('Average fitness')
#         ax.plot(x_data, y_data, '-o')
#         plt.pause(0.5)


# class PlotReporter(neat.reporting.BaseReporter):
#     def __init__(self):
#         self.generation = 0

#     def post_evaluate(self, config, population, species, best_genome):
#         total_fitness = sum(genome.fitness for genome in population.values())
#         avg_fitness = total_fitness / len(population)
#         x_data.append(self.generation)
#         y_data.append(avg_fitness)
#         self.generation += 1


config_path = "config-feedforward.txt"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)


def eval_genomes(genomes, config, screen, generations):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game(screen=screen, generation=generations[0])  # Use the value in the list
        fitness, _ = game.loop(player='ai', net=net)
        genome.fitness = fitness
    
    generations[0] += 1  # Increment the value at the end of each generation

    
        
def run_neat(save_model_name, generations, screen, config=config):
    
    # plot_thread = threading.Thread(target=update_plot)
    # plot_thread.start()
    
    # plot_reporter = PlotReporter()
    
    p = neat.Population(config)
    #p.add_reporter(neat.StdOutReporter(True))
    #p.add_reporter(plot_reporter)
    #stats = neat.StatisticsReporter()
    #p.add_reporter(stats)
    # plt.show(block=False)

    gen = [0]
    eval_function_with_screen = partial(eval_genomes, screen=screen, generations=gen)

    winner = p.run(eval_function_with_screen, generations)
    
    #visualize.draw_net(config, winner, True)
    
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)
    
    #plt.close()
    
    with open(save_model_name, 'wb') as output:
        pickle.dump(winner, output, 1)
        
    return winner


def run_with_best_genome(screen, config=config, file_name='best_genome.pkl'):
    with open(file_name, 'rb') as input_file:
        best_genome = pickle.load(input_file) 

    net = neat.nn.FeedForwardNetwork.create(best_genome, config=config)
    game = Game(screen=screen)
    game.loop(player='ai', net=net, showcase=True)
