class GameConfig:
    """
    Holds configuration settings for the Snake game layout and visual appearance.

    This class centralizes game-related constants, such as grid size, element size,
    color themes, and UI positioning. It allows easy adjustment and access to key values
    used across rendering and logic.

    Attributes
    ----------
    element_size : int
        Size (in pixels) of each individual square (snake segment, apple, etc.).
    grid_size_x : int
        Number of horizontal tiles on the game board.
    grid_size_y : int
        Number of vertical tiles on the game board.
    game_board_loc_x : int
        X-coordinate (in pixels) of the top-left corner of the game board.
    game_board_loc_y : int
        Y-coordinate (in pixels) of the top-left corner of the game board.
    primary_color : str
        Hex color code for the checkerboard tiles.
    secondary_color : str
        Hex color code for borders and accents.
    highlight_color : str
        Hex color code for the main game area background.
    hover_color : str
        Hex color code used when buttons are hovered over.
    score_display_loc_x : int
        X-coordinate for the score display.
    score_display_loc_y : int
        Y-coordinate for the score display.
    """

    def __init__(self):
        self.element_size = 35
        self.grid_size_x = 21
        self.grid_size_y = 12
        self.game_board_loc_x = 34
        self.game_board_loc_y = 145

        self.primary_color = "#89ac46"
        self.secondary_color = "#4d6127"
        self.highlight_color = "#d3e671"
        self.hover_color = "#889a66"

        self.score_display_loc_x = 314
        self.score_display_loc_y = 14
