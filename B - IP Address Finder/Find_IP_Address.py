import tkinter as tk
from tkinter import messagebox, ttk
import socket as s
import os

# File to store history
HISTORY_FILE = "history.txt"

# Function to load history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return [tuple(line.strip().split(", ")) for line in file.readlines()]
    return []

# Function to save history to file
def save_history():
    with open(HISTORY_FILE, "w") as file:
        for entry in history:
            file.write(f"{entry[0]}, {entry[1]}\n")

# History list to store hostnames and IP addresses
history = load_history()

# Function to get and display hostname and IP address
def display_host_ip():
    my_hostname = s.gethostname()
    my_ip = s.gethostbyname(my_hostname)
    result_label.config(text=f"Your Hostname: {my_hostname}\nYour IP Address: {my_ip}")

# Function to get IP address for website
def find_ip():
    host = site_input.get()
    if not host:
        messagebox.showerror("Input Error", "Please enter a valid website.")
        return
    try:
        ip = s.gethostbyname(host)
        result_label.config(text=f"The IP Address of {host} is:\n{ip}")

        # Add to history (newest entry first)
        history.insert(0, (host, ip))
        save_history()  # Save the updated history to file
    except s.gaierror:
        messagebox.showerror("Error", "Invalid hostname or unable to resolve IP.")

# Function to show the history of hostname and IP addresses in a table
def show_history():
    if not history:
        messagebox.showinfo("History", "No history available.")
        return

    # Create a new window for the history table
    history_window = tk.Toplevel(root)
    history_window.title("History of Hostname and IP Lookups")

    # Add a table to display the history
    tree = ttk.Treeview(history_window, columns=("Hostname", "IP Address"), show="headings")
    tree.heading("Hostname", text="Hostname")
    tree.heading("IP Address", text="IP Address")

    # Insert the history into the table (newest first)
    for entry in history:
        tree.insert("", "end", values=entry)

    # Add a scrollbar to the table
    tree.pack(padx=10, pady=10)
    scrollbar = tk.Scrollbar(history_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.config(yscrollcommand=scrollbar.set)

    # Make the history copyable
    def copy_to_clipboard(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0])["values"]
            history_string = f"Hostname: {values[0]}, IP Address: {values[1]}"
            root.clipboard_clear()
            root.clipboard_append(history_string)
            root.update()  # Update clipboard
            messagebox.showinfo("Copied", f"Copied: {history_string}")

    tree.bind("<Double-1>", copy_to_clipboard)

# Adjusting the window size to accommodate the new button
root = tk.Tk()
root.title("IP Finder")

window_width = 500  # Increased width
window_height = 400  # Increased height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
root.config(bg="#f0f0f0")

title_label = tk.Label(root, text="IP Finder", font=("Arial", 18, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

host_ip_button = tk.Button(root, text="Show My Hostname & IP", command=display_host_ip, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", width=20)
host_ip_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f0f0", justify=tk.LEFT)
result_label.pack(pady=20)

site_input_label = tk.Label(root, text="Enter a website (e.g., github.com):", font=("Arial", 12), bg="#f0f0f0")
site_input_label.pack()

site_input = tk.Entry(root, font=("Arial", 12), width=30, relief="sunken", bd=2)
site_input.pack(pady=5)

find_ip_button = tk.Button(root, text="Find IP for Website", command=find_ip, font=("Arial", 12), bg="#008CBA", fg="white", relief="raised", width=20)
find_ip_button.pack(pady=10)

history_button = tk.Button(root, text="Show History", command=show_history, font=("Arial", 12), bg="#FFC107", fg="white", relief="raised", width=20)
history_button.pack(pady=10)

root.mainloop()
