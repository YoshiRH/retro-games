import tkinter as tk
from tkinter import font
from game_app import start_snake, start_tetris, start_pong

def show_menu():
    for widget in root.winfo_children():
        widget.destroy()

    # Create Canva on the entire app window
    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack()

    # Set image as a background
    canvas.create_image(app_center_x, app_center_y, image=background_image)

    # Game title
    canvas.create_text(app_center_x, 64, text="Retro Games\nCollections", font=nunito_bold, fill="#361706", justify="center")

    # Choose game label
    line_length = 150
    canvas.create_line(100, 170, 100 + line_length, 170, fill="#361706", width=3)
    canvas.create_text(app_center_x, 170, text="Choose a game to play", font=nunito_regular, fill="#361706",
                       justify="center")
    canvas.create_line(700 - line_length, 170, 700, 170, fill="#361706", width=3)



    # label = tk.Label(root, text="Wybierz grę", font=("Arial", 14))
    # label.pack(pady=10)
    #
    # btn_snake = tk.Button(root, text="Snake", command=show_snake, width=20)
    # btn_snake.pack(pady=5)
    #
    # btn_tetris = tk.Button(root, text="Tetris", command=show_tetris, width=20)
    # btn_tetris.pack(pady=5)
    #
    # btn_pong = tk.Button(root, text="Pong", command=show_pong, width=20)
    # btn_pong.pack(pady=5)
    #
    # btn_exit = tk.Button(root, text="Wyjdź", command=root.quit, width=20)
    # btn_exit.pack(pady=10)

def show_snake():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Gra Snake", font=("Arial", 14))
    label.pack(pady=10)

    btn_back = tk.Button(root, text="Powrót do menu", command=show_menu, width=20)
    btn_back.pack(pady=10)

    start_snake()

def show_tetris():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Gra Tetris", font=("Arial", 14))
    label.pack(pady=10)

    btn_back = tk.Button(root, text="Powrót do menu", command=show_menu, width=20)
    btn_back.pack(pady=10)

    start_tetris()

def show_pong():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Gra Pong", font=("Arial", 14))
    label.pack(pady=10)

    btn_back = tk.Button(root, text="Powrót do menu", command=show_menu, width=20)
    btn_back.pack(pady=10)

    start_pong()

root = tk.Tk()
root.title("Retro Games")
root.geometry("800x600")
root.resizable(False, False)

app_center_x = 400
app_center_y = 300

background_image = tk.PhotoImage(file="media/menuBackground.png")
nunito_bold = font.Font(family="Nunito", size=28, weight="bold")
nunito_regular = font.Font(family="Nunito", size=18, weight="bold")

show_menu()

root.mainloop()