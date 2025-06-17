import pygame, random
from pygame.math import Vector2

class Snake:
    def __init__(self, element_size, loc_x, loc_y):
        self.element_size = element_size
        self.loc_x = loc_x
        self.loc_y = loc_y

        self.body = [Vector2(5, 6), Vector2(4, 6), Vector2(3, 6)]
        self.direction = Vector2(1, 0)
        self.grow = False

        self.body_sprite = pygame.image.load('media/snake/body.png').convert_alpha()
        self.head_sprite = pygame.image.load('media/snake/head.png').convert_alpha()
        self.tail_sprite = pygame.image.load('media/snake/tail.png').convert_alpha()
        self.turn_sprite = pygame.image.load('media/snake/turn.png').convert_alpha()

    def try_change_direction(self, new_direction):
        if not self.body[0] + new_direction == self.body[1]:
            self.direction = new_direction

    def draw(self, screen):
        for index, coordinates in enumerate(self.body):
            rectangle = pygame.Rect(
                self.loc_x + (coordinates.x * self.element_size),
                self.loc_y + (coordinates.y * self.element_size),
                self.element_size, self.element_size
            )

            sprite = None
            if index == 0:
                sprite = self.rotate_head()
            elif index == len(self.body) - 1:
                sprite = self.rotate_tail()
            else:
                previous_difference = self.body[index + 1] - self.body[index]
                next_difference = self.body[index - 1] - self.body[index]

                if previous_difference.x == next_difference.x:
                    sprite = self.body_sprite
                elif previous_difference.y == next_difference.y:
                    sprite = pygame.transform.rotate(self.body_sprite, 90)
                else:
                    sprite = self.get_turn_sprite(previous_difference, next_difference)

            if sprite:
                screen.blit(sprite, rectangle)
            else:
                pygame.draw.rect(screen, "#F8ED8C", rectangle)

    def rotate_head(self):
        rotation = self.body[1] - self.body[0]
        if rotation == Vector2(0, 1):
            return self.head_sprite
        elif rotation == Vector2(1, 0):
            return pygame.transform.rotate(self.head_sprite, 90)
        elif rotation == Vector2(0, -1):
            return pygame.transform.rotate(self.head_sprite, 180)
        elif rotation == Vector2(-1, 0):
            return pygame.transform.rotate(self.head_sprite, 270)

    def rotate_tail(self):
        rotation = self.body[-2] - self.body[-1]
        if rotation == Vector2(0, 1):
            return self.tail_sprite
        elif rotation == Vector2(1, 0):
            return pygame.transform.rotate(self.tail_sprite, 90)
        elif rotation == Vector2(0, -1):
            return pygame.transform.rotate(self.tail_sprite, 180)
        elif rotation == Vector2(-1, 0):
            return pygame.transform.rotate(self.tail_sprite, 270)

    def get_turn_sprite(self, prev, next_):
        if (prev.x == 1 and next_.y == -1) or (prev.y == -1 and next_.x == 1):
            return pygame.transform.rotate(self.turn_sprite, 0)
        elif (prev.x == -1 and next_.y == -1) or (prev.y == -1 and next_.x == -1):
            return pygame.transform.rotate(self.turn_sprite, 90)
        elif (prev.x == -1 and next_.y == 1) or (prev.y == 1 and next_.x == -1):
            return pygame.transform.rotate(self.turn_sprite, 180)
        elif (prev.x == 1 and next_.y == 1) or (prev.y == 1 and next_.x == 1):
            return pygame.transform.rotate(self.turn_sprite, 270)

    def move(self):
        if self.grow:
            self.grow = False
        else:
            self.body.pop()
        self.body.insert(0, self.body[0] + self.direction)

class Apple:
    def __init__(self, element_size, grid_size_x, grid_size_y, loc_x, loc_y):
        self.element_size = element_size
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.position = self.generate_random_position()

    def generate_random_position(self):
        return Vector2(
            random.randint(0, self.grid_size_x - 1),
            random.randint(0, self.grid_size_y - 1)
        )

    def draw(self, screen):
        rectangle = pygame.Rect(
            self.loc_x + (self.position.x * self.element_size),
            self.loc_y + (self.position.y * self.element_size),
            self.element_size, self.element_size
        )
        image = pygame.image.load('media/snake/apple.png').convert_alpha()
        screen.blit(image, rectangle)

    def reposition(self, snake):
        self.position = self.generate_random_position()
        for coordinates in snake.body:
            if coordinates == self.position:
                self.reposition(snake)