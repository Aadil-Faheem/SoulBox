import psutil
import tkinter as tk
from tkinter import ttk, messagebox, Menu, simpledialog
from datetime import datetime
import threading
import time


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskWatch")
        self.root.geometry("900x550")

        self.processes = []
        self.refresh_interval = 5000
        self.sort_order = {
            "PID": True,
            "Name": True,
            "CPU": True,
            "Memory": True,
            "Status": True,
            "Command Line": True,
        }

        self.dark_mode = False

        # Frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Process info
        self.tree = ttk.Treeview(
            self.frame,
            columns=("PID", "Name", "CPU", "Memory", "Status", "Command Line"),
            show="headings"
        )
        self.tree.heading("PID", text="PID", command=lambda: self.sort_column("PID"))
        self.tree.heading("Name", text="Process Name", command=lambda: self.sort_column("Name"))
        self.tree.heading("CPU", text="CPU Usage", command=lambda: self.sort_column("CPU"))
        self.tree.heading("Memory", text="Memory Usage", command=lambda: self.sort_column("Memory"))
        self.tree.heading("Status", text="Status", command=lambda: self.sort_column("Status"))
        self.tree.heading("Command Line", text="Command Line", command=lambda: self.sort_column("Command Line"))

        self.tree.tag_configure('high', background='#ffcccc')    # High: Red
        self.tree.tag_configure('medium', background='#fff5cc')  # Medium: Yellow
        self.tree.tag_configure('low', background='#ccffcc')     # Low: Green

        # Right-click
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Show CPU Usage", command=self.show_cpu_usage)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Search bar
        self.search_label = ttk.Label(self.root, text="Search:")
        self.search_label.pack(pady=(10, 0))
        self.search_entry = ttk.Entry(self.root)
        self.search_entry.pack(pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_processes)

        # Buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=(0, 10))

        self.refresh_button = ttk.Button(self.button_frame, text="Refresh", command=self.refresh_process_list)
        self.refresh_button.grid(row=0, column=0, padx=10, pady=5)

        self.kill_button = ttk.Button(self.button_frame, text="Kill Process", command=self.kill_process)
        self.kill_button.grid(row=0, column=1, padx=10, pady=5)

        self.log_button = ttk.Button(self.button_frame, text="Log Once", command=self.log_selected_process)
        self.log_button.grid(row=1, column=0, padx=10, pady=5)

        self.track_button = ttk.Button(self.button_frame, text="Log Over Time", command=self.track_process_over_time)
        self.track_button.grid(row=1, column=1, padx=10, pady=5)

        # Dark/Light mode
        self.mode_button = ttk.Button(self.root, text="Toggle Dark/Light Mode", command=self.toggle_mode)
        self.mode_button.pack(pady=(0, 10))

        # Dropdown - refresh rate
        self.refresh_label = ttk.Label(self.root, text="Refresh Interval:")
        self.refresh_label.pack()
        self.refresh_var = tk.StringVar(value="5000")
        self.refresh_dropdown = ttk.Combobox(self.root, textvariable=self.refresh_var, values=["2000", "5000", "10000"])
        self.refresh_dropdown.pack(pady=(0, 10))
        self.refresh_dropdown.bind("<<ComboboxSelected>>", self.change_refresh_interval)

        # Footer
        self.footer = ttk.Label(self.root, text="Made by Aadil Faheem", anchor="center", font=("TkDefaultFont", 9, "italic"))
        self.footer.pack(pady=10)

        self.update_processes()

    def toggle_mode(self):
        bg = "#2e2e2e" if not self.dark_mode else "SystemButtonFace"
        fg = "white" if not self.dark_mode else "black"
        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.configure(background=bg, foreground=fg)
            except:
                pass
        self.dark_mode = not self.dark_mode

    def log_selected_process(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        pid = self.tree.item(selected_item[0])['values'][0]
        for proc in self.processes:
            if proc['pid'] == pid:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_text = f"[{timestamp}] PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, Mem: {proc['memory_info'].rss / (1024*1024):.2f} MB\n"
                with open("process_log.txt", "a") as log_file:
                    log_file.write(log_text)
                messagebox.showinfo("Logged", "Process details logged.")
                break

    def track_process_over_time(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        pid = self.tree.item(selected_item[0])['values'][0]
        try:
            duration = simpledialog.askinteger("Track Duration", "Enter duration in seconds:", minvalue=1, maxvalue=3600)
            if not duration:
                return

            def log_for_duration():
                for i in range(duration):
                    try:
                        proc = psutil.Process(pid)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_text = f"[{timestamp}] PID: {proc.pid}, Name: {proc.name()}, CPU: {proc.cpu_percent(interval=1)}%, Mem: {proc.memory_info().rss / (1024*1024):.2f} MB\n"
                        with open("process_log.txt", "a") as log_file:
                            log_file.write(log_text)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break
                messagebox.showinfo("Done", f"Tracking for PID {pid} completed.")

            threading.Thread(target=log_for_duration).start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_refresh_interval(self, event):
        try:
            self.refresh_interval = int(self.refresh_var.get())
        except ValueError:
            self.refresh_interval = 5000

    def refresh_process_list(self):
        self.tree.delete(*self.tree.get_children())
        self.processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'cmdline']):
            try:
                info = proc.info
                info['status'] = info.get('status', 'Unknown')
                info['name'] = info.get('name', 'N/A')
                info['cpu_percent'] = info.get('cpu_percent', 0.0)
                info['memory_info'] = info.get('memory_info') or psutil._common.smem(rss=0, vms=0)
                info['cmdline'] = info.get('cmdline', [])
                self.processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        self.processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

        for proc in self.processes:
            memory_usage = f"{proc['memory_info'].rss / (1024 * 1024):.2f} MB"
            cpu_val = proc['cpu_percent']
            command_line = " ".join(proc['cmdline']) if proc['cmdline'] else "N/A"
            tag = 'high' if cpu_val >= 50 else 'medium' if cpu_val >= 20 else 'low'
            self.tree.insert("", "end", values=(
                proc['pid'], proc['name'], f"{cpu_val:.2f}%", memory_usage, proc['status'], command_line
            ), tags=(tag,))

    def update_processes(self):
        self.refresh_process_list()
        self.root.after(self.refresh_interval, self.update_processes)

    def kill_process(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        pid = self.tree.item(selected_item[0])['values'][0]
        try:
            psutil.Process(pid).terminate()
            self.refresh_process_list()
            messagebox.showinfo("Success", f"Process {pid} terminated successfully.")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", f"Process {pid} no longer exists.")
        except psutil.AccessDenied:
            messagebox.showerror("Access Denied", "You do not have permission to terminate this process.")
        except psutil.ZombieProcess:
            messagebox.showerror("Error", f"Process {pid} is a zombie process and cannot be terminated.")

    def sort_column(self, col):
        reverse = self.sort_order[col]
        self.sort_order[col] = not reverse
        key_map = {
            "PID": lambda x: x['pid'],
            "Name": lambda x: x['name'].lower(),
            "CPU": lambda x: x['cpu_percent'],
            "Memory": lambda x: x['memory_info'].rss,
            "Status": lambda x: x['status'],
            "Command Line": lambda x: " ".join(x['cmdline']) if x['cmdline'] else ""
        }
        self.processes.sort(key=key_map[col], reverse=reverse)

        self.tree.delete(*self.tree.get_children())
        for proc in self.processes:
            memory_usage = f"{proc['memory_info'].rss / (1024 * 1024):.2f} MB"
            cpu_val = proc['cpu_percent']
            command_line = " ".join(proc['cmdline']) if proc['cmdline'] else "N/A"
            tag = 'high' if cpu_val >= 50 else 'medium' if cpu_val >= 20 else 'low'
            self.tree.insert("", "end", values=(
                proc['pid'], proc['name'], f"{cpu_val:.2f}%", memory_usage, proc['status'], command_line
            ), tags=(tag,))

    def filter_processes(self, event):
        search_term = self.search_entry.get().lower()
        filtered = [p for p in self.processes if search_term in p['name'].lower() or search_term in str(p['pid'])]

        self.tree.delete(*self.tree.get_children())
        for proc in filtered:
            memory_usage = f"{proc['memory_info'].rss / (1024 * 1024):.2f} MB"
            cpu_val = proc['cpu_percent']
            command_line = " ".join(proc['cmdline']) if proc['cmdline'] else "N/A"
            tag = 'high' if cpu_val >= 50 else 'medium' if cpu_val >= 20 else 'low'
            self.tree.insert("", "end", values=(
                proc['pid'], proc['name'], f"{cpu_val:.2f}%", memory_usage, proc['status'], command_line
            ), tags=(tag,))

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.context_menu.post(event.x_root, event.y_root)

    def show_cpu_usage(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        pid = self.tree.item(selected_item[0])['values'][0]
        process = psutil.Process(pid)
        cpu_usage = process.cpu_percent(interval=1)
        messagebox.showinfo("CPU Usage", f"Process {pid} CPU Usage: {cpu_usage}%")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
