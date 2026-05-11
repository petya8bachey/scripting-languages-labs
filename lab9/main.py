import tkinter as tk

def handle_click():
    label.config(text=f"Результат: {entry.get()}")

root = tk.Tk()
root.title("Лабораторная №9")
root.geometry("250x140")

entry = tk.Entry(root, width=28)
entry.pack(pady=8)

btn = tk.Button(root, text="Обработать", command=handle_click)
btn.pack(pady=5)

label = tk.Label(root, text="Ожидание ввода...")
label.pack(pady=8)

root.mainloop()