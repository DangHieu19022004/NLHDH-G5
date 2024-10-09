import time
from datetime import datetime, timedelta

from plyer import notification


class Event:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

def schedule_reminder(events):
    # Sắp xếp các sự kiện theo thời gian bắt đầu
    events.sort(key=lambda event: event.start_time)

    for event in events:
        now = datetime.now()
        time_until_event = (event.start_time - now).total_seconds()

        if time_until_event > 0:
            print(f"Sự kiện '{event.name}' sẽ bắt đầu vào {event.start_time}. Chờ {int(time_until_event)} giây.")
            time.sleep(time_until_event)  # Chờ cho đến khi sự kiện bắt đầu

        # Hiển thị thông báo
        notification.notify(
            title="Nhắc nhở",
            message=f"Sự kiện '{event.name}' đang diễn ra!",
            app_name="Lịch nhắc nhở",
            timeout=10  # Thời gian hiển thị thông báo (giây)
        )

        # Thời gian chờ cho đến khi sự kiện kết thúc
        event_duration = (event.end_time - event.start_time).total_seconds()
        time.sleep(event_duration)

        # Hiển thị thông báo khi sự kiện hoàn thành
        notification.notify(
            title="Thông báo",
            message=f"Sự kiện '{event.name}' đã hoàn thành lúc {event.end_time}.",
            app_name="Lịch nhắc nhở",
            timeout=10
        )

if __name__ == "__main__":
    # Ví dụ sự kiện
    event_list = [
        Event("Cuộc họp", datetime.now() + timedelta(seconds=5), datetime.now() + timedelta(seconds=15)),
        Event("Thảo luận dự án", datetime.now() + timedelta(seconds=20), datetime.now() + timedelta(seconds=30)),
        Event("Nghỉ trưa", datetime.now() + timedelta(seconds=35), datetime.now() + timedelta(seconds=45)),
    ]

    schedule_reminder(event_list)
