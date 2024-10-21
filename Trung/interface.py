import threading
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from plyer import notification
from win10toast import ToastNotifier
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

class Event:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lịch Nhắc Nhở")
        self.root.geometry('500x550')
        self.root.configure(bg='#87CEFA')

        # Setup the interface
        self.setup_interface()

        # List of events
        self.events = []
        self.notifier = ToastNotifier()

        # System Tray Icon
        self.create_tray_icon()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

    def setup_interface(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 12), padding=10, background="#ff5733", foreground="white")
        style.configure('TLabel', font=('Arial', 10), padding=5, background='#FFFFFF')

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        # Labels and Input Fields
        self.entries = {
            "Tên sự kiện:": ttk.Entry(frame, width=30),
            "Thời gian bắt đầu (HH:MM):": ttk.Entry(frame, width=30),
            "Thời gian kết thúc (HH:MM):": ttk.Entry(frame, width=30)
        }
        for i, (label_text, entry) in enumerate(self.entries.items()):
            ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry.grid(row=i, column=1, pady=5)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Thêm sự kiện", command=self.add_event).grid(row=0, column=1, padx=5)
        self.button_event_list = ttk.Button(button_frame, text="Chưa thêm sự kiện", state=tk.DISABLED, command=self.show_event_list)
        self.button_event_list.grid(row=0, column=0, padx=5)

    def add_event(self):
        try:
            name = self.entries["Tên sự kiện:"].get()
            start_time = datetime.strptime(self.entries["Thời gian bắt đầu (HH:MM):"].get(), "%H:%M")
            end_time = datetime.strptime(self.entries["Thời gian kết thúc (HH:MM):"].get(), "%H:%M")
            today = datetime.now()
            start_time = today.replace(hour=start_time.hour, minute=start_time.minute, second=0)
            end_time = today.replace(hour=end_time.hour, minute=end_time.minute, second=0)

            if end_time <= start_time or start_time <= today:
                raise ValueError("Thời gian không hợp lệ.")

            self.events.append(Event(name, start_time, end_time))
            messagebox.showinfo("Thông báo", f"Sự kiện '{name}' đã được thêm!")
            self.clear_entries()
            self.button_event_list.config(text="Danh sách sự kiện đã tạo", state=tk.NORMAL)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def show_event_list(self):
        event_list_window = tk.Toplevel(self.root)
        event_list_window.title("Danh sách sự kiện")
        event_list_window.geometry("400x350")
        
        search_frame = tk.Frame(event_list_window)
        search_frame.pack(pady=10)

        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm kiếm", command=lambda: self.search_events(search_entry.get())).pack(side=tk.LEFT, padx=5)

        self.event_listbox = tk.Listbox(event_list_window, selectmode=tk.SINGLE, width=50)
        self.event_listbox.pack(pady=10)
        self.update_event_listbox(self.events)

    def search_events(self, keyword):
        matched_events = [event for event in self.events if keyword.lower() in event.name.lower()]
        self.update_event_listbox(matched_events)

    def update_event_listbox(self, events):
        self.event_listbox.delete(0, tk.END)
        for event in events:
            self.event_listbox.insert(tk.END, f"{event.name} (Từ: {event.start_time.strftime('%H:%M')} Đến: {event.end_time.strftime('%H:%M')})")

    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color=(73, 109, 137))
        draw = ImageDraw.Draw(image)
        draw.text((10, 20), "RM", fill="white")
        menu = Menu(MenuItem('Mở lại ứng dụng', self.show_window), MenuItem('Thoát', self.quit))
        self.tray_icon = Icon("Lịch Nhắc Nhở", image, "Lịch Nhắc Nhở", menu)

    def hide_window(self):
        self.root.withdraw()
        self.tray_icon.run()

    def show_window(self):
        self.root.deiconify()
        self.tray_icon.stop()

    def quit(self):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
