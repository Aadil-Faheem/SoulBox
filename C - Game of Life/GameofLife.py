import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ON = 255
OFF = 0
vals = [ON, OFF]

class GameOfLifeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")
        self.grid_size = 50
        self.update_interval = 100
        self.pattern = "Random"
        self.grid = None

        self.create_menu()

    def create_menu(self):
        self.clear_window()

        # Set window size and center it
        self.root.geometry("600x600")  # 1:1 ratio and reduced size
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        title = tk.Label(self.frame, text="Conway's Game of Life", font=("Helvetica", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=30)  # Increased space from the rest

        tk.Label(self.frame, text="Grid Size:").grid(row=1, column=0, pady=10)
        self.grid_entry = tk.Entry(self.frame)
        self.grid_entry.insert(0, "50")
        self.grid_entry.grid(row=1, column=1, pady=10)

        tk.Label(self.frame, text="Update Interval (ms):").grid(row=2, column=0, pady=10)
        self.interval_entry = tk.Entry(self.frame)
        self.interval_entry.insert(0, "100")
        self.interval_entry.grid(row=2, column=1, pady=10)

        tk.Label(self.frame, text="Initial Pattern:").grid(row=3, column=0, pady=10)
        self.pattern_var = tk.StringVar(value="Random")
        pattern_menu = ttk.Combobox(self.frame, textvariable=self.pattern_var)
        pattern_menu['values'] = ("Random", "Glider", "Gosper Gun", "Exploder", "Small Exploder")
        pattern_menu.grid(row=3, column=1, pady=10)

        tk.Button(self.frame, text="Start Simulation", command=self.start_simulation).grid(row=4, column=0, columnspan=2, pady=20)

        # Gray italic text at the bottom
        footer = tk.Label(self.root, text="Created by Aadil Faheem", font=("Helvetica", 10, "italic"), fg="gray")
        footer.pack(side="bottom", pady=10)

    def start_simulation(self):
        try:
            self.grid_size = int(self.grid_entry.get())
            self.update_interval = int(self.interval_entry.get())
            self.pattern = self.pattern_var.get()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for grid size and interval.")
            return

        self.clear_window()
        self.grid = np.zeros((self.grid_size, self.grid_size))

        if self.pattern == "Random":
            self.grid = np.random.choice(vals, self.grid_size*self.grid_size, p=[0.2, 0.8]).reshape(self.grid_size, self.grid_size)
        elif self.pattern == "Glider":
            self.add_glider(1, 1)
        elif self.pattern == "Gosper Gun":
            self.add_gosper_glider_gun(10, 10)
        elif self.pattern == "Exploder":
            self.add_exploder(10, 10)
        elif self.pattern == "Small Exploder":
            self.add_small_exploder(10, 10)

        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.grid, interpolation='nearest')
        self.ani = animation.FuncAnimation(self.fig, self.update, fargs=(self.img,), frames=10, interval=self.update_interval, save_count=50)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

        tk.Button(self.root, text="Back to Menu", command=self.create_menu).pack(pady=10)

    def update(self, frameNum, img):
        newGrid = self.grid.copy()
        N = self.grid_size
        for i in range(N):
            for j in range(N):
                total = int((self.grid[i, (j-1)%N] + self.grid[i, (j+1)%N] +
                            self.grid[(i-1)%N, j] + self.grid[(i+1)%N, j] +
                            self.grid[(i-1)%N, (j-1)%N] + self.grid[(i-1)%N, (j+1)%N] +
                            self.grid[(i+1)%N, (j-1)%N] + self.grid[(i+1)%N, (j+1)%N])/255)

                if self.grid[i, j] == ON:
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = OFF
                else:
                    if total == 3:
                        newGrid[i, j] = ON

        img.set_data(newGrid)
        self.grid[:] = newGrid[:]
        return img,

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_glider(self, i, j):
        glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
        self.grid[i:i+3, j:j+3] = glider

    def add_gosper_glider_gun(self, i, j):
        gun = np.zeros((11, 38))
        coords = [
            (5,1),(5,2),(6,1),(6,2),(3,13),(3,14),(4,12),(4,16),(5,11),(5,17),
            (6,11),(6,15),(6,17),(6,18),(7,11),(7,17),(8,12),(8,16),(9,13),(9,14),
            (1,25),(2,23),(2,25),(3,21),(3,22),(4,21),(4,22),(5,21),(5,22),
            (6,23),(6,25),(7,25),(3,35),(3,36),(4,35),(4,36)
        ]
        for x, y in coords:
            gun[x, y] = ON
        self.grid[i:i+11, j:j+38] = gun

    def add_exploder(self, i, j):
        pattern = [
            (0,0),(0,2),(0,4),
            (1,0),(1,4),
            (2,0),(2,4),
            (3,0),(3,4),
            (4,0),(4,2),(4,4)
        ]
        for dx, dy in pattern:
            self.grid[i+dx, j+dy] = ON

    def add_small_exploder(self, i, j):
        pattern = [
            (0,1),
            (1,0),(1,1),(1,2),
            (2,0),(2,2),
            (3,1)
        ]
        for dx, dy in pattern:
            self.grid[i+dx, j+dy] = ON


if __name__ == '__main__':
    root = tk.Tk()
    app = GameOfLifeApp(root)
    root.mainloop()
