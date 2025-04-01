import tkinter as tk
import subprocess
import sys


def start_snake():
    subprocess.Popen([sys.executable, "snake.py"])

def start_pong():
    subprocess.Popen([sys.executable, "pong.py"])


root = tk.Tk()
root.title("Klasyczne Gry")
root.geometry("800x600")
root.resizable(False, False)


label = tk.Label(root, text="Wybierz grę", font=("Arial", 14))
label.pack(pady=10)


btn_snake = tk.Button(root, text="Snake", command=start_snake, width=20)
btn_snake.pack(pady=5)

btn_pong = tk.Button(root, text="Pong", command=start_pong, width=20)
btn_pong.pack(pady=5)


btn_exit = tk.Button(root, text="Wyjdź", command=root.quit, width=20)
btn_exit.pack(pady=10)


root.mainloop()