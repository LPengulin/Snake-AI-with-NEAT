import pygame


class Snake:
    
    def __init__(self, color, width, height, x, y):
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.segments = [pygame.Rect(self.x, self.y, self.width, self.height)]
        self.direction = (1, 0)
        self.speed = 10
        self.should_grow = False
        
    
    def set_direction(self, dx, dy):
        if self.direction == (-dx, -dy):
            return
        self.direction = (dx, dy)
        
    
    def move(self):
        
        if self.should_grow:
            last_segment_position = self.segments[-1].topleft
        
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i-1].x
            self.segments[i].y = self.segments[i-1].y
        
        dx, dy = self.direction
        self.segments[0].x += dx * self.speed
        self.segments[0].y += dy * self.speed
        
        if self.should_grow:
            new_segment = pygame.Rect(last_segment_position, (self.width, self.height))
            self.segments.append(new_segment)
            self.should_grow = False
    
    def grow(self):
        self.should_grow = True
        
        
    #bug with this method, returns has collided with self if colliding with food
    #fixed, turns out the bug was related to the snake's speed and its height and width
    #adding segment if the speed not a multiple of 10 will cause the new segment to collide with the second last segment
    # def _grow_segment(self):
    #     last_segment = self.segments[-1].copy()
        
    #     if self.direction == (0, -1):
    #         last_segment.y -= self.height
    #     elif self.direction == (0, 1):
    #         last_segment.y += self.height
    #     elif self.direction == (1, 0):
    #         last_segment.x += self.width
    #     elif self.direction == (-1, 0):
    #         last_segment.x -= self.width
            
    #     self.segments.append(last_segment)   
     
    
    def has_collided_with_self(self):
        head = self.segments[0]
        for index, segment in enumerate(self.segments[1:]):
            if head.colliderect(segment):
                return True

        return False

    
    
    def draw(self, screen):
        for iDx, segment in enumerate(self.segments):
            pygame.draw.rect(screen, self.color, segment)
        