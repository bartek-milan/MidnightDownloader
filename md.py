import tkinter as tk
import time
import threading
import os
import numpy as np
import cv2
from PIL import ImageGrab
import tkinter.messagebox as messagebox

MIN_WIDTH = 100
MIN_HEIGHT = 50
RESIZE_MARGIN = 20
TOP_EXTENSION = 15
CHECK_INTERVAL_SEC = 5*60  # minutes you want in seconds or x * 60

class DownloadWatcher:
    def __init__(self):
        self.width = 300
        self.height = 200
        self.x = 300
        self.y = 200
        self.monitoring = False
        self.shutdown_scheduled = False

        self.root = tk.Tk()
        self.root.title("Download Watcher")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'white')
        self.root.configure(bg='white')
        self.set_geometry()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height + TOP_EXTENSION + 20,
                                bg='white', highlightthickness=0)
        self.canvas.pack()

        self.border_thickness = 10

        self.rect = self.canvas.create_rectangle(
            0, TOP_EXTENSION, self.width, self.height + TOP_EXTENSION,
            outline='green', width=self.border_thickness)

        self.top_border_line = self.canvas.create_line(
            0, TOP_EXTENSION, self.width, TOP_EXTENSION, fill='green', width=self.border_thickness)

        self.resize_handle = self.canvas.create_rectangle(
            self.width - RESIZE_MARGIN, self.height + TOP_EXTENSION - RESIZE_MARGIN,
            self.width, self.height + TOP_EXTENSION,
            fill='red', outline='red'
        )

        self.close_button = tk.Button(self.root, text='X', command=self.root.destroy,
                                      bg='red', fg='white', borderwidth=0, font=('Arial', 10, 'bold'),
                                      cursor='hand2')
        self.close_button.place(x=self.width - 25, y=TOP_EXTENSION + 5, width=20, height=20)

        self.start_button = tk.Button(self.root, text='Start', command=self.start_monitoring,
                                      bg='green', fg='white', borderwidth=0, font=('Arial', 10, 'bold'))
        self.start_button.place(x=5, y=TOP_EXTENSION + 5, width=50, height=20)

        text_str = "Created by Milán Bartek"
        self.font = ('Arial', 12, 'bold')
        self.padding_x = 8
        self.padding_y = 4

        temp_text_id = self.canvas.create_text(0, 0, text=text_str, font=self.font, anchor='nw')
        bbox = self.canvas.bbox(temp_text_id)
        self.canvas.delete(temp_text_id)

        self.text_width = bbox[2] - bbox[0]
        self.text_height = bbox[3] - bbox[1]

        text_x = self.width // 2
        text_y = TOP_EXTENSION // 2

        self.outer_rect_coords = (
            text_x - self.text_width // 2 - self.padding_x - 2,
            text_y - self.text_height // 2 - self.padding_y - 2,
            text_x + self.text_width // 2 + self.padding_x + 2,
            text_y + self.text_height // 2 + self.padding_y + 2
        )

        self.inner_rect_coords = (
            text_x - self.text_width // 2 - self.padding_x,
            text_y - self.text_height // 2 - self.padding_y,
            text_x + self.text_width // 2 + self.padding_x,
            text_y + self.text_height // 2 + self.padding_y
        )

        self.text_outer_border = self.canvas.create_rectangle(
            *self.outer_rect_coords,
            fill='green', outline='green', width=1)

        self.text_inner_border = self.canvas.create_rectangle(
            *self.inner_rect_coords,
            fill='black', outline='white', width=1)

        self.text_id = self.canvas.create_text(
            text_x, text_y,
            text=text_str,
            fill='white',
            font=self.font)

        self.resizing = False
        self.moving = False
        self.start_x = 0
        self.start_y = 0

        self.canvas.bind('<Button-1>', self.mouse_down)
        self.canvas.bind('<B1-Motion>', self.mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)

    def set_geometry(self):
        total_height = self.height + TOP_EXTENSION + 20
        self.root.geometry(f'{self.width}x{total_height}+{self.x}+{self.y}')

    def in_corner(self, x, y):
        return x >= self.width - RESIZE_MARGIN and y >= self.height + TOP_EXTENSION - RESIZE_MARGIN

    def mouse_down(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        if self.in_corner(event.x, event.y):
            self.resizing = True
        else:
            self.moving = True

    def mouse_drag(self, event):
        dx = event.x_root - self.start_x
        dy = event.y_root - self.start_y

        if self.resizing:
            new_width = max(MIN_WIDTH, self.width + dx)
            new_height = max(MIN_HEIGHT, self.height + dy)
            self.width = new_width
            self.height = new_height
            self.set_geometry()
            self.canvas.config(width=self.width, height=self.height + TOP_EXTENSION + 20)
            self.canvas.coords(self.rect, 0, TOP_EXTENSION, self.width, self.height + TOP_EXTENSION)
            self.canvas.coords(self.top_border_line, 0, TOP_EXTENSION, self.width, TOP_EXTENSION)
            self.canvas.coords(self.resize_handle,
                               self.width - RESIZE_MARGIN, self.height + TOP_EXTENSION - RESIZE_MARGIN,
                               self.width, self.height + TOP_EXTENSION)

            text_x = self.width // 2
            text_y = TOP_EXTENSION // 2

            self.outer_rect_coords = (
                text_x - self.text_width // 2 - self.padding_x - 2,
                text_y - self.text_height // 2 - self.padding_y - 2,
                text_x + self.text_width // 2 + self.padding_x + 2,
                text_y + self.text_height // 2 + self.padding_y + 2
            )
            self.canvas.coords(self.text_outer_border, *self.outer_rect_coords)

            self.inner_rect_coords = (
                text_x - self.text_width // 2 - self.padding_x,
                text_y - self.text_height // 2 - self.padding_y,
                text_x + self.text_width // 2 + self.padding_x,
                text_y + self.text_height // 2 + self.padding_y
            )
            self.canvas.coords(self.text_inner_border, *self.inner_rect_coords)

            self.canvas.coords(self.text_id, text_x, text_y)

            self.close_button.place(x=self.width - 25, y=TOP_EXTENSION + 5)
            self.start_button.place(x=5, y=TOP_EXTENSION + 5)

        elif self.moving:
            self.x += dx
            self.y += dy
            self.set_geometry()

        self.start_x = event.x_root
        self.start_y = event.y_root

    def mouse_up(self, event):
        self.resizing = False
        self.moving = False

    def capture_screenshot(self):
        left = self.x
        top = self.y + TOP_EXTENSION + 20
        right = self.x + self.width
        bottom = self.y + TOP_EXTENSION + 20 + self.height
        img = ImageGrab.grab(bbox=(left, top, right, bottom))
        img_gray = img.convert('L')  # grayscale
        return np.array(img_gray)

    def compare_images(self, img1, img2):
        diff = cv2.absdiff(img1, img2)
        changed_pixels = np.sum(diff > 10)
        total_pixels = diff.size
        percent_diff = (changed_pixels / total_pixels) * 100
        print(f"Change: {percent_diff:.2f}%")
        return percent_diff

    def schedule_shutdown(self):
        if not self.shutdown_scheduled:
            self.shutdown_scheduled = True
            print("Shutdown scheduled: your PC will shut down in 15 minutes.")
            messagebox.showinfo("Shutdown Scheduled", "Your PC will shut down in 15 minutes. \n Thank you for using my software ^^ ")
            time.sleep(15 * 60)
            os.system("shutdown /s /t 0")

    def monitor_loop(self):
        baseline = self.capture_screenshot()
        print("Baseline screenshot taken.")
        while self.monitoring and not self.shutdown_scheduled:
            time.sleep(CHECK_INTERVAL_SEC)

            current_img = self.capture_screenshot()
            diff = self.compare_images(baseline, current_img)

            if diff < 2.0:
                print("Download likely complete. Scheduling shutdown in 15 minutes...")
                self.schedule_shutdown()
                break
            else:
                baseline = current_img

    def start_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            threading.Thread(target=self.monitor_loop, daemon=True).start()
            print("Monitoring started.")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    DownloadWatcher().run()
