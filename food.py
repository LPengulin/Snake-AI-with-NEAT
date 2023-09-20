import pygame
import random


class Food:
    
    WIDTH = 10
    HEIGHT = 10
    
    def __init__(self, screen_width, screen_height, color):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = color
        self.body = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.respawn()
    
    
    def respawn(self):
        self.x = random.randint(0, self.screen_width - self.WIDTH)
        self.y = random.randint(0, self.screen_height - self.HEIGHT)
        self.body.topleft = (self.x, self.y)
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.body)
        
   
    def is_eaten_by(self, snake):
        return self.body.colliderect(snake.segments[0])