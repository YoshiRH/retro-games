import pygame, random
from pygame.math import Vector2
from collections import deque

class Snake:
    """
    Represents the snake in the Snake game.

    Handles movement, growth, direction queueing, and drawing the snake
    with appropriate sprites based on orientation and state.

    Parameters
    ----------
    element_size : int
        Size of a single grid element (in pixels).
    loc_x : int
        X-coordinate of the top-left corner of the game board.
    loc_y : int
        Y-coordinate of the top-left corner of the game board.
    grid_size_x : int
        Number of horizontal tiles in the game grid.
    grid_size_y : int
        Number of vertical tiles in the game grid.
    """

    def __init__(self, element_size, loc_x, loc_y, grid_size_x, grid_size_y):
        self.body = [Vector2(5, 6), Vector2(4, 6), Vector2(3, 6)]
        self.direction_queue = deque()
        self.alive = True

        self.direction = Vector2(1, 0)
        self.grow = False

        self._element_size = element_size
        self._loc_x = loc_x
        self._loc_y = loc_y
        self._grid_size_x = grid_size_x
        self._grid_size_y = grid_size_y

        self._body_sprite = pygame.image.load('media/snake/body.png').convert_alpha()
        self._head_sprite = pygame.image.load('media/snake/head.png').convert_alpha()
        self._tail_sprite = pygame.image.load('media/snake/tail.png').convert_alpha()
        self._turn_sprite = pygame.image.load('media/snake/turn.png').convert_alpha()
        self._dead_sprite = pygame.image.load('media/snake/dead.png').convert_alpha()

    def queue_direction(self, new_dir):
        """
        Queues a new direction for the snake, ignoring 180° reversals.

        Parameters
        ----------
        new_dir : Vector2
            The direction to queue (e.g., Vector2(1, 0) for right).
        """
        if len(self.direction_queue) == 0:
            last_dir = self.direction
        else:
            last_dir = self.direction_queue[-1]

        if new_dir + last_dir != Vector2(0, 0):  # Prevent 180° reversal
            self.direction_queue.append(new_dir)

    def move(self):
        """
        Moves the snake one step in the current direction.

        If growth is active, the tail is not removed.
        """
        if self.direction_queue:
            self.direction = self.direction_queue.popleft()

        self.body.insert(0, self.body[0] + self.direction)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()

    def draw(self, screen):
        """
        Draws the snake on the given screen surface.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the snake on.
        """
        for index, segment in enumerate(self.body):
            rect = self._get_rect_for_segment(segment)

            if index == 0:
                sprite = self._get_head_sprite()
            elif index == len(self.body) - 1:
                sprite = self._get_tail_sprite()
            else:
                sprite = self._get_middle_sprite(index)

            screen.blit(sprite, rect) if sprite else pygame.draw.rect(screen, "#F8ED8C", rect)

    def _get_rect_for_segment(self, segment):
        """
        Calculates the pixel rectangle for a grid segment.

        Converts a grid-based coordinate (Vector2) to a pixel-based `pygame.Rect`
        suitable for rendering.

        Parameters
        ----------
        segment : Vector2
            The position on the grid.

        Returns
        -------
        pygame.Rect
            The pixel rectangle representing the segment.
        """
        return pygame.Rect(
            self._loc_x + segment.x * self._element_size,
            self._loc_y + segment.y * self._element_size,
            self._element_size,
            self._element_size)

    def _get_head_sprite(self):
        """
        Selects and rotates the appropriate head sprite based on movement direction.

        If the snake is dead, returns the rotated dead head sprite instead.

        Returns
        -------
        pygame.Surface
            The rotated head (or dead) sprite surface.
        """
        direction = self.body[1] - self.body[0]
        sprite = self._head_sprite if self.alive else self._dead_sprite
        return self._rotate_sprite(sprite, direction)

    def _get_tail_sprite(self):
        """
        Selects and rotates the tail sprite based on the direction from the last two body segments.

        Returns
        -------
        pygame.Surface
            The rotated tail sprite surface.
        """
        direction = self.body[-2] - self.body[-1]
        return self._rotate_sprite(self._tail_sprite, direction)

    def _get_middle_sprite(self, index):
        """
        Determines the appropriate sprite for a middle segment of the snake's body.

        Based on the directions between neighboring segments, chooses a straight or turn sprite,
        and applies necessary rotation.

        Parameters
        ----------
        index : int
            Index of the current segment in the snake's body.

        Returns
        -------
        pygame.Surface or None
            The appropriate body sprite surface, or None if a valid direction pattern isn't matched.
        """
        prev_dir = self.body[index + 1] - self.body[index]
        next_dir = self.body[index - 1] - self.body[index]

        # Straight pieces
        if prev_dir.x == next_dir.x:
            return self._body_sprite  # Vertical
        elif prev_dir.y == next_dir.y:
            return pygame.transform.rotate(self._body_sprite, 90)  # Horizontal

        # Turns
        if (prev_dir.x == 1 and next_dir.y == -1) or (prev_dir.y == -1 and next_dir.x == 1):
            return pygame.transform.rotate(self._turn_sprite, 0)
        elif (prev_dir.x == -1 and next_dir.y == -1) or (prev_dir.y == -1 and next_dir.x == -1):
            return pygame.transform.rotate(self._turn_sprite, 90)
        elif (prev_dir.x == -1 and next_dir.y == 1) or (prev_dir.y == 1 and next_dir.x == -1):
            return pygame.transform.rotate(self._turn_sprite, 180)
        elif (prev_dir.x == 1 and next_dir.y == 1) or (prev_dir.y == 1 and next_dir.x == 1):
            return pygame.transform.rotate(self._turn_sprite, 270)

        return None  # Fallback (shouldn't be reached)

    @staticmethod
    def _rotate_sprite(sprite, direction):
        """
        Rotates a given sprite surface to match a movement direction.

        Parameters
        ----------
        sprite : pygame.Surface
            The sprite image to rotate.
        direction : Vector2
            The direction to rotate the sprite toward (e.g., Vector2(0, 1) for down).

        Returns
        -------
        pygame.Surface
            The rotated sprite surface.
        """
        if direction == Vector2(0, 1): return sprite
        elif direction == Vector2(1, 0): return pygame.transform.rotate(sprite, 90)
        elif direction == Vector2(0, -1): return pygame.transform.rotate(sprite, 180)
        elif direction == Vector2(-1, 0): return pygame.transform.rotate(sprite, 270)

class Apple:
    """
    Represents an apple that the snake can collect.

    Responsible for generating a random valid position on the board
    and rendering itself.

    Parameters
    ----------
    element_size : int
        Size of a single grid element (in pixels).
    grid_size_x : int
        Number of horizontal tiles in the grid.
    grid_size_y : int
        Number of vertical tiles in the grid.
    loc_x : int
        X-coordinate of the top-left corner of the game board.
    loc_y : int
         Y-coordinate of the top-left corner of the game board.
    """

    def __init__(self, element_size, grid_size_x, grid_size_y, loc_x, loc_y):
        self._element_size = element_size
        self._grid_size_x = grid_size_x
        self._grid_size_y = grid_size_y
        self._loc_x = loc_x
        self._loc_y = loc_y
        self._image = pygame.image.load('media/snake/apple.png').convert_alpha()

        self.position = self._generate_random_position()

    def reposition(self, snake):
        """
        Repositions the apple to a random location not occupied by the snake.

        Parameters
        ----------
        snake : Snake
            The current snake object, used to avoid placing the apple on its body.
        """
        while True:
            self.position = self._generate_random_position()
            if self.position not in snake.body:
                break

    def draw(self, screen):
        """
        Draws the apple on the game screen.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the apple on.
        """
        rectangle = pygame.Rect(
            self._loc_x + (self.position.x * self._element_size),
            self._loc_y + (self.position.y * self._element_size),
            self._element_size, self._element_size
        )
        screen.blit(self._image, rectangle)

    def _generate_random_position(self):
        """
        Generates a new random position for the apple within the game grid.

        Returns
        -------
        Vector2
            A random position within the grid bounds.
        """
        return Vector2(
            random.randint(0, self._grid_size_x - 1),
            random.randint(0, self._grid_size_y - 1))