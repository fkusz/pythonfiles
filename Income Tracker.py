import tkinter as tk
import time

class Counter:
    def __init__(self, master, hourly_rate):
        self.master = master
        self.rate = hourly_rate/3600
        master.title("Counter")

        self.label = tk.Label(master, text="0", font=("Arial", 96))
        self.label.pack()

        self.start_time = time.time()
        self.update_clock()

    def update_clock(self):
        elapsed_time = (time.time() - self.start_time)*self.rate
        self.label.configure(text="${:.4f}".format(elapsed_time))
        self.master.after(10, self.update_clock)
        
root = tk.Tk()
counter = Counter(root,60)
counter2 = Counter(root,7.25)
root.mainloop()