from game import Game
from agent import run_neat, run_with_best_genome
import pygame
import pygame_menu
import os
import pickle
#run_with_best_genome()
#run_neat()

#game = Game()
#game.loop(player='human')

pygame.init()
surface = pygame.display.set_mode((1280, 720))
icon = pygame.image.load(os.path.join(os.getcwd(), 'images', 'icon.png'))
pygame.display.set_icon(icon)
game = Game(screen=surface)
trained_model_name = 'trained_model.pkl'
showcase_model = 'best_genome.pkl'
generations = 1

high_score_human = game.load_high_score()
high_score_ai = game.load_high_score(player_type='ai')



def update_high_scores():
    global high_score_human, high_score_ai
    high_score_human = game.load_high_score()
    high_score_ai = game.load_high_score(player_type='ai')


def set_generations(value, difficulty):
    global generations
    generations = value[0][1]

def start_game():
    game.loop(player='human')
    update_high_scores()
    create_menu()

def load_trained_model():
    if os.path.exists(os.path.join(os.getcwd(), trained_model_name)):
        run_with_best_genome(surface, file_name=trained_model_name)
        update_high_scores()
        create_menu()
        
def showcase():
    run_with_best_genome(surface, file_name=showcase_model)

def train_model():
    run_neat(save_model_name=trained_model_name, generations=generations, screen=surface)
    
    
def create_menu():
    menu = pygame_menu.Menu('Snake AI Trainer', 1280, 720, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label(title=f"Player highscore: {high_score_human}")
    menu.add.label(title=f"Ai highscore: {high_score_ai}")

    menu.add.button('Play', start_game)
    menu.add.button('Showcase', showcase)
    menu.add.button('Load trained model', load_trained_model)
    menu.add.selector('Num generations: ', [('25', 25), ('50', 50), ('75', 75), ('100', 100)], onchange=set_generations)
    menu.add.button('Train model', train_model)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)


if __name__ == "__main__":
    
    create_menu()