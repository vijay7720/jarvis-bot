import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class JarvisUI:
    def __init__(self, on_command):
        self.on_command = on_command


        self.root = tk.Tk()
        self.root.title("Jarvis Assistant")
        self.root.geometry("500x600")


        self.chat_area = ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(expand=True, fill='both', padx=10, pady=10)


        self.entry = tk.Entry(self.root, font=("Arial", 12))
        self.entry.pack(fill='x', padx=10)
        self.entry.bind('<Return>', self.submit)


        self.status = tk.Label(self.root, text="🟢 Jarvis Ready", anchor='w')
        self.status.pack(fill='x', padx=10, pady=5)


    def start(self):
        self.root.mainloop()


    def submit(self, event=None):
        text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.add_message(f"🧑 You: {text}")
        self.on_command(text)


    def add_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)


    def set_status(self, text):
        self.status.config(text=text)