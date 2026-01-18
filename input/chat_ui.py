import tkinter as tk

def start_chat(on_command):
    def submit():
        text = entry.get()
        entry.delete(0, tk.END)
        on_command(text)

    root = tk.Tk()
    root.title("Jarvis")

    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=10)

    tk.Button(root, text="Send", command=submit).pack()

    root.mainloop()
