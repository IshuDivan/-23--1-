import threading
import keyboard
import time
from datetime import datetime

# Определите требуемую комбинацию клавиш для завершения
REQUIRED_KEYS = {'ctrl', 'shift'}
BAD_KEYS = {'z', 'x', 'c'}


class KeyCombinationTracker:
    def __init__(self, required_keys):
        self.required_keys = set(required_keys)
        self.pressed_keys = set()

    def add_key(self, key):
        self.pressed_keys.add(key)

    def remove_key(self, key):
        self.pressed_keys.discard(key)

    def is_combination_pressed(self):
        return self.required_keys.issubset(self.pressed_keys)


class Observer:
    def __init__(self, subscribers):
        self.subscribers = subscribers

    def on_next(self, value, event_type):
        for subscriber in self.subscribers:
            subscriber.on_next(value, event_type)

    def on_completed(self):
        for subscriber in self.subscribers:
            subscriber.on_completed()

    def on_error(self, e):
        for subscriber in self.subscribers:
            subscriber.on_error(e)


class ErrorSubscriber:
    def __init__(self, thread_id):
        self.thread_id = thread_id
        self.error_count = 0

    def on_next(self, value, event_type):
        pass

    def on_completed(self):
        # print(f"ErrorSubscriber {self.thread_id}: Monitoring completed.")
        # print(f"Total error count: {self.error_count}")
        pass

    def on_error(self, e):
        # self.error_count += 1
        # print(f"ErrorSubscriber {self.thread_id}: Monitoring error occurred: {e}")
        pass


class WritingSubscriber:
    def __init__(self, thread_id, filename):
        self.thread_id = thread_id
        self.filename = filename
        self.key_count = 0

    def on_next(self, value, event_type):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_entry = f"Thread {self.thread_id} - {current_time}: Key {event_type}: {value}\n"
        with open(self.filename, 'a') as file:
            file.write(log_entry)

        self.key_count += 1
        print(log_entry.strip())

    def on_completed(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_entry = f"Thread {self.thread_id} - {current_time}: detection finished\n"
        with open(self.filename, 'a') as file:
            file.write(log_entry)
        print(log_entry.strip())

    def on_error(self, e):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_entry = f"Thread {self.thread_id} - {current_time}: error detected:\n\t{e}\n"
        with open(self.filename, 'a') as file:
            file.write(log_entry)
        print(log_entry.strip())


def monitor_keys(observer, key_combination_tracker):
    is_running = True

    while is_running:
        events = keyboard.read_event()
        if events:
            key = events.name
            if events.event_type == keyboard.KEY_DOWN:
                event_type = 'pressed'
                key_combination_tracker.add_key(key)
            elif events.event_type == keyboard.KEY_UP:
                event_type = 'released'
                key_combination_tracker.remove_key(key)
            else:
                continue

            if key_combination_tracker.is_combination_pressed():
                is_running = False
                observer.on_completed()
                continue

            observer.on_next(key, event_type)

            if key in BAD_KEYS and events.event_type == keyboard.KEY_DOWN:
                observer.on_error(f"Error: Bad key '{key}' pressed.")


def main():
    output_file = "keys0.txt"
    with open(output_file, 'w') as f:
        f.write('Starting logging:\n')

    writing_subscriber1 = WritingSubscriber(thread_id=1, filename=output_file)
    writing_subscriber2 = WritingSubscriber(thread_id=2, filename=output_file)
    error_subscriber = ErrorSubscriber(thread_id=3)

    key_combination_tracker = KeyCombinationTracker(REQUIRED_KEYS)

    subscribers = [writing_subscriber1, writing_subscriber2, error_subscriber]
    observer = Observer(subscribers)

    print(f"Программа запущена. Для завершения нажмите {' + '.join(REQUIRED_KEYS)}")

    key_thread = threading.Thread(target=monitor_keys, args=(observer, key_combination_tracker))
    key_thread.start()

    key_thread.join()

    print("Программа завершена.")


if __name__ == "__main__":
    main()