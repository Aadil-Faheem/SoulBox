import tkinter as tk
from tkinter import messagebox

# Conversion rate
CONVERSION_RATE = 0.0001  # 1 Schrute Buck = $0.0001

def convert_to_usd():
    try:
        schrute_bucks = float(entry.get())
        real_dollars = schrute_bucks * CONVERSION_RATE
        result_label.config(text=f"{schrute_bucks} Schrute Bucks = ${real_dollars:.6f} USD")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number.")

def convert_to_schrute():
    try:
        usd = float(entry.get())
        schrute_bucks = usd / CONVERSION_RATE
        result_label.config(text=f"${usd:.2f} USD = {schrute_bucks:.0f} Schrute Bucks")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number.")

# GUI setup
root = tk.Tk()
root.title("Schrute Buck Converter")
root.geometry("420x320")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Title
title = tk.Label(root, text="💵 Schrute Buck Converter 💰", font=("Arial", 16, "bold"), bg="#f0f0f0")
title.pack(pady=15)

# Quote
quote = tk.Label(root, text='"One Schrute Buck is equal to one one-hundredth of a cent."', font=("Arial", 9, "italic"), bg="#f0f0f0", fg="gray25", wraplength=350, justify="center")
quote.pack(pady=2)

# Entry field
entry = tk.Entry(root, font=("Arial", 14), justify="center")
entry.pack(pady=15)
entry.insert(0, "1000")

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack()

to_usd_btn = tk.Button(button_frame, text="→ Convert to USD", font=("Arial", 11), bg="#4CAF50", fg="white", width=18, command=convert_to_usd)
to_usd_btn.grid(row=0, column=0, padx=5)

to_schrute_btn = tk.Button(button_frame, text="← Convert to Schrute Bucks", font=("Arial", 11), bg="#2196F3", fg="white", width=22, command=convert_to_schrute)
to_schrute_btn.grid(row=0, column=1, padx=5)

# Result display
result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0", fg="black")
result_label.pack(pady=20)

# Footer
footer = tk.Label(root, text="Made by Aadil Faheem", font=("Arial", 9, "italic"), fg="gray", bg="#f0f0f0")
footer.pack(side="bottom", pady=5)

root.mainloop()
