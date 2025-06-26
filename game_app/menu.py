import tkinter as tk
from tkinter import font
from game_app import start_snake, start_tetris, start_pong

def create_game_box(canvas, x, y, title, image_path=None, on_click=None):
    # Default values for box
    box_size = 160
    border_width = 3
    padding = 8
    border_color = "#DB7E39"
    bg_color = "#C4A684"
    hover_color = "#A88A68"
    text_color = "#361706"
    divider_color = "#361706"

    # Store ID
    box_tag = f"game_box_{x}_{y}"

    # Draw box
    box_id = canvas.create_rectangle(x, y, x + box_size, y + box_size, outline=border_color, width=border_width, fill=bg_color, tags=box_tag)

    # Title
    title_font = font.Font(family="Nunito", size=16, weight="bold")
    title_bg_id = canvas.create_rectangle(x + padding, y + padding, x + box_size - padding, y + padding + 30,
                                          fill=bg_color, outline="", tags=box_tag)
    canvas.create_text(x + box_size / 2, y + padding + 15, text=title, font=title_font, fill=text_color,
                       justify="center", tags=box_tag)

    # Divider
    canvas.create_line(x + padding, y + padding + 30, x + box_size - padding, y + padding + 30, fill=divider_color,
                       width=1, tags=box_tag)

    # Content
    if image_path:
        image = tk.PhotoImage(file=image_path)
        canvas.create_image(x + box_size / 2, y + (box_size + padding + 30) / 2, image=image, tags=box_tag)
        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.append(image)

    # Hover effects
    canvas.tag_bind(box_tag, "<Enter>", lambda event: [canvas.itemconfig(box_id, fill=hover_color),
                                                       canvas.itemconfig(title_bg_id, fill=hover_color)])
    canvas.tag_bind(box_tag, "<Leave>", lambda event: [canvas.itemconfig(box_id, fill=bg_color),
                                                       canvas.itemconfig(title_bg_id, fill=bg_color)])

    # OnClick Event
    if on_click:
        canvas.tag_bind(box_tag, "<Button-1>", lambda event: on_click())

def draw_menu_base(canvas):
    # Set image as a background
    canvas.create_image(app_center_x, app_center_y, image=background_image)

    # Menu logo
    canvas.create_image(app_center_x, 66, image=menu_logo_image)

    # Choose game label
    line_length = 150
    canvas.create_line(100, 170, 100 + line_length, 170, fill="#361706", width=3)
    canvas.create_text(app_center_x, 170, text="Choose a game to play", font=nunito_regular, fill="#361706",
                       justify="center")
    canvas.create_line(700 - line_length, 170, 700, 170, fill="#361706", width=3)

def show_menu():
    for widget in root.winfo_children():
        widget.destroy()

    # Create Canvas on the entire app window
    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack()

    draw_menu_base(canvas)

    create_game_box(canvas, 100, 210, "Tetris", "media/tetrisPreview.png", show_tetris)
    create_game_box(canvas, 320, 210, "Snake", "media/snakePreview.png", show_snake)
    create_game_box(canvas, 540, 210, "Pong", "media/pongPreview.png", show_pong)

    # Exit button
    exit_button_image = tk.PhotoImage(file="media/exitButton.png")
    exit_button_image_hover = tk.PhotoImage(file="media/exitButtonHover.png")

    exit_button_id = canvas.create_image(app_center_x, 500, image=exit_button_image, tags="exit_button")

    if not hasattr(canvas, 'images'):
        canvas.images = []
    canvas.images.append(exit_button_image)
    canvas.images.append(exit_button_image_hover)

    canvas.tag_bind("exit_button", "<Button-1>", lambda event: root.quit())
    canvas.tag_bind("exit_button", "<Enter>",
                    lambda event: canvas.itemconfig(exit_button_id, image=exit_button_image_hover))
    canvas.tag_bind("exit_button", "<Leave>", lambda event: canvas.itemconfig(exit_button_id, image=exit_button_image))

def show_snake():
    for widget in root.winfo_children():
        widget.destroy()

    start_snake(root)
    show_menu()

def show_tetris():
    for widget in root.winfo_children():
        widget.destroy()

    start_tetris(root)
    show_menu()

def show_pong():
    for widget in root.winfo_children():
        widget.destroy()

    start_pong(root)
    show_menu()

root = tk.Tk()
root.title("Retro Games")
root.geometry("800x600")
root.resizable(False, False)

app_center_x = 400
app_center_y = 300

background_image = tk.PhotoImage(file="media/menuBackground.png")
menu_logo_image = tk.PhotoImage(file="media/menuLogo.png")

nunito_bold = font.Font(family="Nunito", size=28, weight="bold")
nunito_regular = font.Font(family="Nunito", size=18, weight="bold")

show_menu()

root.mainloop()