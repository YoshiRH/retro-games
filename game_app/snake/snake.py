import pygame, random
from pygame.math import Vector2
from collections import deque

class Snake:
    def __init__(self, element_size, loc_x, loc_y, grid_size_x, grid_size_y):
        self.element_size = element_size
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y

        self.body = [Vector2(5, 6), Vector2(4, 6), Vector2(3, 6)]
        self.direction = Vector2(1, 0)
        self.grow = False

        self.body_sprite = pygame.image.load('media/snake/body.png').convert_alpha()
        self.head_sprite = pygame.image.load('media/snake/head.png').convert_alpha()
        self.tail_sprite = pygame.image.load('media/snake/tail.png').convert_alpha()
        self.turn_sprite = pygame.image.load('media/snake/turn.png').convert_alpha()
        self.dead_sprite = pygame.image.load('media/snake/dead.png').convert_alpha()

        self.direction_queue = deque()
        self.alive = True

    def queue_direction(self, new_dir):
        if len(self.direction_queue) == 0:
            last_dir = self.direction
        else:
            last_dir = self.direction_queue[-1]

        if new_dir + last_dir != Vector2(0, 0):  # Prevent 180° reversal
            self.direction_queue.append(new_dir)

    def move(self):
        if self.direction_queue:
            self.direction = self.direction_queue.popleft()

        self.body.insert(0, self.body[0] + self.direction)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()

    def draw(self, screen):
        for index, segment in enumerate(self.body):
            rect = self.get_rect_for_segment(segment)

            if index == 0:
                sprite = self.get_head_sprite()
            elif index == len(self.body) - 1:
                sprite = self.get_tail_sprite()
            else:
                sprite = self.get_middle_sprite(index)

            screen.blit(sprite, rect) if sprite else pygame.draw.rect(screen, "#F8ED8C", rect)

    def get_rect_for_segment(self, segment):
        return pygame.Rect(
            self.loc_x + segment.x * self.element_size,
            self.loc_y + segment.y * self.element_size,
            self.element_size,
            self.element_size)

    def get_head_sprite(self):
        direction = self.body[1] - self.body[0]
        sprite = self.head_sprite if self.alive else self.dead_sprite
        return self.rotate_sprite(sprite, direction)

    def get_tail_sprite(self):
        direction = self.body[-2] - self.body[-1]
        return self.rotate_sprite(self.tail_sprite, direction)

    def get_middle_sprite(self, index):
        prev_dir = self.body[index + 1] - self.body[index]
        next_dir = self.body[index - 1] - self.body[index]

        # Straight pieces
        if prev_dir.x == next_dir.x:
            return self.body_sprite  # Vertical
        elif prev_dir.y == next_dir.y:
            return pygame.transform.rotate(self.body_sprite, 90)  # Horizontal

        # Turns
        if (prev_dir.x == 1 and next_dir.y == -1) or (prev_dir.y == -1 and next_dir.x == 1):
            return pygame.transform.rotate(self.turn_sprite, 0)
        elif (prev_dir.x == -1 and next_dir.y == -1) or (prev_dir.y == -1 and next_dir.x == -1):
            return pygame.transform.rotate(self.turn_sprite, 90)
        elif (prev_dir.x == -1 and next_dir.y == 1) or (prev_dir.y == 1 and next_dir.x == -1):
            return pygame.transform.rotate(self.turn_sprite, 180)
        elif (prev_dir.x == 1 and next_dir.y == 1) or (prev_dir.y == 1 and next_dir.x == 1):
            return pygame.transform.rotate(self.turn_sprite, 270)

        return None  # Fallback (shouldn't be reached)

    @staticmethod
    def rotate_sprite(sprite, direction):
        if direction == Vector2(0, 1): return sprite
        elif direction == Vector2(1, 0): return pygame.transform.rotate(sprite, 90)
        elif direction == Vector2(0, -1): return pygame.transform.rotate(sprite, 180)
        elif direction == Vector2(-1, 0): return pygame.transform.rotate(sprite, 270)

class Apple:
    def __init__(self, element_size, grid_size_x, grid_size_y, loc_x, loc_y):
        self.element_size = element_size
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.position = self.generate_random_position()
        self.image = pygame.image.load('media/snake/apple.png').convert_alpha()

    def draw(self, screen):
        rectangle = pygame.Rect(
            self.loc_x + (self.position.x * self.element_size),
            self.loc_y + (self.position.y * self.element_size),
            self.element_size, self.element_size
        )
        screen.blit(self.image, rectangle)

    def reposition(self, snake):
        while True:
            self.position = self.generate_random_position()
            if self.position not in snake.body:
                break

    def generate_random_position(self):
        return Vector2(
            random.randint(0, self.grid_size_x - 1),
            random.randint(0, self.grid_size_y - 1))