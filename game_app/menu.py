import tkinter as tk
from game_app import start_snake, start_tetris, start_pong

def show_menu():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Wybierz grę", font=("Arial", 14))
    label.pack(pady=10)

    btn_snake = tk.Button(root, text="Snake", command=show_snake, width=20)
    btn_snake.pack(pady=5)

    btn_tetris = tk.Button(root, text="Tetris", command=show_tetris, width=20)
    btn_tetris.pack(pady=5)

    btn_pong = tk.Button(root, text="Pong", command=show_pong, width=20)
    btn_pong.pack(pady=5)

    btn_exit = tk.Button(root, text="Wyjdź", command=root.quit, width=20)
    btn_exit.pack(pady=10)

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

show_menu()

root.mainloop()