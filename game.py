import pygame
import pickle
import os
from snake import Snake
from food import Food

pygame.init()
pygame.font.init()


class Game:
    
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    
    COLORS = {
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
        'green': (0, 255, 0),
        'black': (0, 0, 0),
        'white': (255, 255, 255)
    }
    
    HIGH_SCORE_HUMAN = "human_high_score.pkl"
    HIGH_SCORE_AI = "ai_high_score.pkl"
    
    def __init__(self, screen, generation=0) -> None:
        self.title = "Snake"
        self.SCREEN = screen
        self.generation = generation
    
    
    def save_high_score(self, score, player_type='human'):
        if player_type == 'human':
            file_name = self.HIGH_SCORE_HUMAN
        else:
            file_name = self.HIGH_SCORE_AI
            
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                existing_high_score = pickle.load(f)
                if score > existing_high_score:
                    with open(file_name, 'wb') as f:
                        pickle.dump(score, f)
        else:
            with open(file_name, 'wb') as f:
                pickle.dump(score, f)
                
    def load_high_score(self, player_type='human'):
        if player_type == 'human':
            file_name = self.HIGH_SCORE_HUMAN
        else:
            file_name = self.HIGH_SCORE_AI
            
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                return pickle.load(f)
            
        return 0
    
    
    def fill(self, color):
        self.SCREEN.fill(color)
        
        
    def update(self):
        pygame.display.flip()
        
    
    def draw_score(self, score):
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f'Score: {score}', True, self.COLORS['white'])
        score_rect = score_surface.get_rect(topleft=(10, 10))
        self.SCREEN.blit(score_surface, score_rect)
    
    def draw_generation(self, generation):
        font = pygame.font.Font(None, 36)
        generation_surface = font.render(f'Generation: {generation}', True, self.COLORS['white'])
        gen_rect_center = generation_surface.get_rect(center=(self.WINDOW_WIDTH // 2, 30))
        self.SCREEN.blit(generation_surface, gen_rect_center.topleft)

        
    def get_game_state(self, snake, food, hunger_rate):
        
        distance_to_food_x = food.x - snake.segments[0].x
        distance_to_food_y = food.y - snake.segments[0].y
        distance_to_wall_x = self.WINDOW_WIDTH - snake.segments[0].x 
        distance_to_wall_y = self.WINDOW_HEIGHT - snake.segments[0].y
        
        # #distance_of_segments_from_head = [(snake.segments[i].x - snake.segments[0].x, snake.segments[i].y - snake.segments[0].y) for i in range(1, len(snake.segments))]
        
        return [distance_to_food_x, distance_to_food_y, snake.segments[0].x, snake.segments[0].y, distance_to_wall_x, distance_to_wall_y, hunger_rate]
    
    
        # # distance_to_food_x = (food.x - snake.segments[0].x) / self.WINDOW_WIDTH
        # # distance_to_food_y = (food.y - snake.segments[0].y) / self.WINDOW_HEIGHT
        # # snake_pos_x = snake.segments[0].x / self.WINDOW_WIDTH
        # # snake_pos_y = snake.segments[0].y / self.WINDOW_HEIGHT

        # # return [distance_to_food_x, distance_to_food_y, snake_pos_x, snake_pos_y]
        
        # normalized_distance_to_food_x = distance_to_food_x / self.WINDOW_WIDTH
        # normalized_distance_to_food_y = distance_to_food_y / self.WINDOW_HEIGHT
        # normalized_snake_head_x = snake.segments[0].x / self.WINDOW_WIDTH
        # normalized_snake_head_y = snake.segments[0].y / self.WINDOW_HEIGHT
        # normalized_distance_to_wall_x = distance_to_wall_x / self.WINDOW_WIDTH
        # normalized_distance_to_wall_y = distance_to_wall_y / self.WINDOW_HEIGHT
        # max_hunger = 1000
        # normalized_hunger_rate = hunger_rate / max_hunger
        
        # return [normalized_distance_to_food_x, normalized_distance_to_food_y, normalized_snake_head_x, normalized_snake_head_y, normalized_distance_to_wall_x, normalized_distance_to_wall_y
        #         ,normalized_hunger_rate]
        
        
    
    def determine_direction(self, action_outputs):
        max_value_index = action_outputs.index(max(action_outputs))
        
        if max_value_index == 0:
            return (0, -1) # up
        elif max_value_index == 1:
            return (0, 1) # down
        elif max_value_index == 2:
            return (1, 0) # right
        elif max_value_index == 3:
            return (-1, 0) # left
    
    
    def loop(self, player='human', net=None, showcase=False):
        
        clock = pygame.time.Clock()
        state = True
        
        
        #snake initial position
        x = self.WINDOW_WIDTH // 2
        y = self.WINDOW_HEIGHT // 2
        
        
        snake = Snake(color=self.COLORS['green'], width=10, height=10, x=x, y=y)
        food = Food(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, color=self.COLORS['red'])
        direction = None
        score = 0
        reward = 0
        hunger_counter = 1000
        
        if player == 'human':
            clock_speed = 60
        elif player == 'ai' and showcase:
            clock_speed = 60
        else:
            clock_speed = 10000
        
        while state:
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = False
                
                if player == 'human':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            snake.set_direction(0, -1)
                        elif event.key == pygame.K_DOWN:
                            snake.set_direction(0, 1)
                        elif event.key == pygame.K_RIGHT:
                            snake.set_direction(1, 0)
                        elif event.key == pygame.K_LEFT:
                            snake.set_direction(-1, 0)
                
            if player == 'ai':
                inputs = self.get_game_state(snake=snake, food=food, hunger_rate=hunger_counter)
                action_outputs = net.activate(inputs)
                direction = self.determine_direction(action_outputs)
                snake.set_direction(direction[0], direction[1])
                
            snake.move()
                        
            if snake.segments[0].left < 0 or snake.segments[0].right > self.WINDOW_WIDTH:
                state = False
                reward -= 10
            if snake.segments[0].top < 0 or snake.segments[0].bottom > self.WINDOW_HEIGHT:
                state = False
                reward -= 10

            if food.is_eaten_by(snake):
                score += 1
                reward += 10
                hunger_counter = 1000
                food.respawn()
                snake.grow()
                
            if snake.has_collided_with_self():
                state = False
                reward -= 15
                
            if hunger_counter <= 0 and player == 'ai':
                state = False
                reward -= 10
            
            #print(snake.segments[0].x)
            #reward -= 1
            self.fill(self.COLORS['black'])
            
            hunger_counter -= 1
            
            snake.draw(self.SCREEN)
            food.draw(self.SCREEN)
            self.draw_score(score)
        
            if player == 'ai' and not showcase:
                self.draw_generation(self.generation+1)
            
            self.update()
            
            clock.tick(clock_speed)
        
        if player == 'human':
            self.save_high_score(score=score)
        elif player == 'ai' and showcase:
            self.save_high_score(score=score, player_type='ai')
        
        return reward, score

              
    