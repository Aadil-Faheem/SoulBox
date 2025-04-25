import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import os
import json

# Function to browse and select Python file
def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")],
        title="Select a Python file"
    )
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# Function to save the Tkinter path for future use
def browse_tkinter_path():
    tkinter_path = filedialog.askdirectory(title="Select Tkinter Library Folder")
    if tkinter_path:
        try:
            with open("tkinter_path.json", "w") as f:
                json.dump({"tkinter_path": tkinter_path}, f)
            messagebox.showinfo("Success", "Tkinter path saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Tkinter path: {e}")

# Function to convert Python file to EXE
def convert_to_exe():
    python_file = entry_file_path.get()

    if not python_file:
        messagebox.showerror("Error", "Please select a Python file first.")
        return

    if not python_file.endswith(".py"):
        messagebox.showerror("Error", "Please select a valid Python (.py) file.")
        return

    try:
        # Check if Tkinter path is saved, if not, ask user to provide it
        if not os.path.exists("tkinter_path.json"):
            messagebox.showerror("Error", "Tkinter path is not saved. Please select the Tkinter library folder first.")
            return
        
        with open("tkinter_path.json", "r") as f:
            tkinter_data = json.load(f)
            tkinter_path = tkinter_data.get("tkinter_path")

        if not tkinter_path:
            messagebox.showerror("Error", "Tkinter path is not valid. Please select it again.")
            return

        # Get the directory of the selected Python file
        file_directory = os.path.dirname(python_file)

        browse_button.config(state=tk.DISABLED)
        convert_button.config(state=tk.DISABLED)
        
        # Prepare the pyinstaller command
        command = [
            'pyinstaller',
            '--onefile',  
            '--windowed',  
            '--distpath', file_directory,  # Output EXE in the same directory as the Python file
            '--workpath', file_directory,  # Use the same directory for the build folder
            '--specpath', file_directory,  # Save the .spec file in the same directory
            '--add-data', f"{tkinter_path}/:tkinter",  # Add Tkinter data for the EXE
            python_file
        ]

        # Run the command in the terminal
        subprocess.run(command, check=True)

        # Show success message
        messagebox.showinfo("Success", f"Conversion successful! EXE is in the same directory as the Python file.")
    
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        browse_button.config(state=tk.NORMAL)
        convert_button.config(state=tk.NORMAL)


root = tk.Tk()
root.title("Python to EXE Converter")

root.configure(bg="#f0f0f0")

frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
frame.pack(padx=40, pady=40)

label = ttk.Label(frame, text="Select Python File:", font=("Helvetica", 12, "bold"), background="#f0f0f0")
label.grid(row=0, column=0, sticky="w", pady=5)

entry_file_path = ttk.Entry(frame, width=40, font=("Helvetica", 12))
entry_file_path.grid(row=1, column=0, padx=5, pady=10)

browse_button = ttk.Button(frame, text="Browse", command=browse_file, style="TButton")
browse_button.grid(row=1, column=1, padx=10)

# Button to browse and save the Tkinter path
tkinter_path_button = ttk.Button(frame, text="Set Tkinter Path", command=browse_tkinter_path, style="TButton")
tkinter_path_button.grid(row=2, column=0, columnspan=2, pady=10)

convert_button = ttk.Button(frame, text="Convert to EXE", command=convert_to_exe, style="TButton")
convert_button.grid(row=3, column=0, columnspan=2, pady=20)

footer_label = ttk.Label(frame, text="Powered by PyInstaller", font=("Helvetica", 10, "italic"), background="#f0f0f0")
footer_label.grid(row=4, column=0, columnspan=2, pady=5)

style = ttk.Style()
style.configure("TButton",
                font=("Helvetica", 12, "bold"),
                padding=10,
                relief="flat",
                background="#4CAF50",
                foreground="black")
style.map("TButton", background=[("active", "green")], foreground=[("active", "green")])  # Button hover effect

root.mainloop()
