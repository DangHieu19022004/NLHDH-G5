import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem
from win10toast import ToastNotifier


class Event:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.notified = False  # Đánh dấu đã gửi thông báo
        self.ended_notified = False  # Đánh dấu đã gửi thông báo kết thúc

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lịch Nhắc Nhở")
        self.root.geometry('500x400')
        self.root.configure(bg='#f0f0f0')

        # Giao diện ứng dụng hiện đại hơn
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=5)
        style.configure('TLabel', font=('Arial', 10), padding=5)

        self.label_event_name = ttk.Label(root, text="Tên sự kiện:")
        self.label_event_name.pack(pady=5)

        self.entry_event_name = ttk.Entry(root)
        self.entry_event_name.pack(pady=5)

        self.label_start_time = ttk.Label(root, text="Thời gian bắt đầu (HH:MM):")
        self.label_start_time.pack(pady=5)

        self.entry_start_time = ttk.Entry(root)
        self.entry_start_time.pack(pady=5)

        self.label_end_time = ttk.Label(root, text="Thời gian kết thúc (HH:MM):")
        self.label_end_time.pack(pady=5)

        self.entry_end_time = ttk.Entry(root)
        self.entry_end_time.pack(pady=5)

        self.button_add_event = ttk.Button(root, text="Thêm sự kiện", command=self.add_event)
        self.button_add_event.pack(pady=10)

        self.events = []
        self.reminder_thread = threading.Thread(target=self.check_reminders, daemon=True)
        self.reminder_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        # Tạo icon cho khay hệ thống
        self.create_tray_icon()

        # Tạo đối tượng cho thông báo Windows
        self.notifier = ToastNotifier()

    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color=(73, 109, 137))
        draw = ImageDraw.Draw(image)
        draw.text((10, 20), "RM", fill="white")

        menu = Menu(
            MenuItem('Mở lại ứng dụng', self.show_window),
            MenuItem('Thoát', self.quit)
        )

        self.tray_icon = Icon("Lịch Nhắc Nhở", image, "Lịch Nhắc Nhở", menu)

    def add_event(self):
        name = self.entry_event_name.get()
        start_time_str = self.entry_start_time.get()
        end_time_str = self.entry_end_time.get()

        try:
            start_time = datetime.strptime(start_time_str, "%H:%M")
            end_time = datetime.strptime(end_time_str, "%H:%M")

            today = datetime.now()
            start_time = today.replace(hour=start_time.hour, minute=start_time.minute, second=0)
            end_time = today.replace(hour=end_time.hour, minute=end_time.minute, second=0)

            if end_time <= start_time:
                raise ValueError("Thời gian kết thúc phải lớn hơn thời gian bắt đầu.")

            if start_time <= today:  # Kiểm tra thời gian bắt đầu
                raise ValueError("Thời gian bắt đầu phải lớn hơn thời gian hiện tại.")

            self.events.append(Event(name, start_time, end_time))
            messagebox.showinfo("Thông báo", f"Sự kiện '{name}' đã được thêm!")
            self.entry_event_name.delete(0, tk.END)
            self.entry_start_time.delete(0, tk.END)
            self.entry_end_time.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))


    def check_reminders(self):
        while True:
            now = datetime.now()



            for event in self.events:
                # Kiểm tra nếu sự kiện đang diễn ra và gửi thông báo "đang diễn ra"
                if event.start_time <= now <= event.end_time:
                    if not event.notified:
                        self.send_notification(event)
                        event.notified = True  # Đánh dấu đã gửi thông báo

                # Kiểm tra nếu sự kiện đã kết thúc và gửi thông báo "hoàn thành"
                elif now > event.end_time:
                    if not event.ended_notified:
                        self.send_end_notification(event)
                        event.ended_notified = True  # Đánh dấu đã gửi thông báo kết thúc
                        self.events.remove(event)  # Xóa sự kiện đã hoàn thành

            time.sleep(10)  # Giảm thời gian chờ xuống 10 giây để cập nhật gần với thời gian thực hơn

    def send_notification(self, event):
        duration = 30  # Thay đổi giá trị này để điều chỉnh thời gian hiển thị
        self.notifier.show_toast(
            "Nhắc nhở",
            f"Sự kiện '{event.name}' đang diễn ra!",
            duration=duration
        )

    def send_end_notification(self, event):
        duration = 30  # Thay đổi giá trị này để điều chỉnh thời gian hiển thị
        self.notifier.show_toast(
            "Thông báo",
            f"Sự kiện '{event.name}' đã hoàn thành lúc {event.end_time.strftime('%H:%M')}.",
            duration=duration
        )


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
